import logging
import requests
import platform
import os
import sys
from configparser import ConfigParser
from pathlib import Path
from .exceptions import UnrecoverableError
from .vm import Vm, Images, SshKey
from .network import Network
from .kube import Kube
from .identity import Identity
from . import __version__ as sdk_version

logger = logging.getLogger(__name__)

DEFAULT_ECHOME_DIR = ".echome"
DEFAULT_ECHOME_SESSION_DIR = ".echome/sess"
DEFAULT_CONFIG_FILE = "config"
DEFAULT_CREDENTIAL_FILE = "credentials"

DEFAULT_PROFILE = "default"
DEFAULT_CONNECTION = "insecure"
API_VERSION = "v1"

# Grabs the config and credentials from the user's home dir
# and establishes a connection with the server and authorization
class Session:

    _token = None
    _refresh = None
    _config_contents = None
    _cred_contents = None

    def __init__(self, profile:str = None, server:str = None, access_id:str = None, 
            secret_key:str = None, protocol:str = None, login:bool = True):
        self.home_dir = str(Path.home())
        echome_dir = f"{self.home_dir}/{DEFAULT_ECHOME_DIR}"

        self.cred_file  = f"{echome_dir}/{DEFAULT_CREDENTIAL_FILE}"
        self.conf_file  = f"{echome_dir}/{DEFAULT_CONFIG_FILE}"

        # Order of preference for values:
        # If the value is set with in class initiation, these will always take precedence.
        # If no values are supplied, we look for environment variables (ECHOME_PROFILE, ECHOME_SERVER, etc.)
        # If neither are set we look at the user's supplied file for config and credentials.
        self.current_profile = self._get(profile, os.getenv("ECHOME_PROFILE", DEFAULT_PROFILE))
        
        self.server_url = self._get(server, os.getenv("ECHOME_SERVER", self.__get_local_config("server")))
        self.access_id  = self._get(access_id, os.getenv("ECHOME_ACCESS_ID", self.__get_local_credentials("access_id")))
        self.secret_key = self._get(secret_key, os.getenv("ECHOME_SECRET_KEY", self.__get_local_credentials("secret_key")))

        # Some values like 'protocol' will default to the DEFAULT_CONNECTION
        # even if it is not supplied anywhere. 
        proto = self.__get_local_config("protocol") 
        self.connection_type = self._get(
            protocol, 
            os.getenv("ECHOME_PROTOCOL", proto if proto else DEFAULT_CONNECTION)
        )

        if self.connection_type == "insecure":
            self.protocol = "http://"
        elif self.connection_type == "secure":
            self.protocol = "https://"
        else:
            raise ConfigFileError(f"Unknown connection type specified. Use either 'secure' or 'insecure'. A blank value defaults to {DEFAULT_CONNECTION}")

        self.API_VERSION = API_VERSION

        if not self.server_url:
            raise UnrecoverableError("ecHome server URL is not set in environment variable or config file. Unable to continue.")
        
        # Setting the base URL: <protocol>://<server-domain-or-ip>/api/<version>
        self.base_url = f"{self.protocol}{self.server_url}/api/{self.API_VERSION}"
        self.user_agent = f"ecHome_sdk/{sdk_version} (Python {platform.python_version()})"

        logger.debug(f"Using base url: {self.base_url}")
        logger.debug(f"Using user agent: {self.user_agent}")

        # try retrieving session tokens we already have by reading the files and setting the variables
        self.load_local_tokens()
        # If the token variable is still empty, log in to set them.
        if login and self._token is None:
            self.login()
        else:
            logger.debug('login set to false, skipping session grabbing')
    
    # Login and retrieve our tokens
    def login(self):
        logger.debug("Logging in to ecHome server")
        logger.debug(f"Using access key: {self.access_id}")
        r = requests.post(
            f"{self.base_url}/identity/token", 
            data={"username": self.access_id, "password": self.secret_key},
            headers=self.build_headers()
        )
        response = r.json()
        if r.status_code == 200 and "access" in response:
            self.token = response["access"]
            self.refresh = response["refresh"]
            return True
        else:
            return False
    
    # refresh the access token using the refresh token
    def refresh_token(self):
        r = requests.post(
            f"{self.base_url}/identity/token/refresh", 
            headers=self.build_headers(self.token),
            data={"refresh": self.refresh}
        )
        response = r.json()
        if r.status_code == 200 and "access" in response:
            self.token = response["access"]
            return True
        else:
            return False
    
    def load_local_tokens(self):
        self.token
        self.refresh
    
    @property
    def token(self): 
        logger.debug("Getting Token") 
        if self._token is None:
            logger.debug("Session _token is empty, attempting to retrieve from local file.")
            self._token = self.__get_session()

        if self._token is None:
            logger.debug("Session _token is still empty!")
        return self._token 
    
    # a setter function 
    @token.setter 
    def token(self, a): 
        logger.debug("Setting Token") 
        self._token = self.__save_session_token(a)
    

    @property
    def refresh(self): 
        logger.debug("Getting Refresh Token") 
        if self._refresh is None:
            logger.debug("Refresh _token is empty, attempting to retrieve from local file.")
            self._refresh = self.__get_session(type="refresh")

        if self._refresh is None:
            logger.debug("Refresh _token is still empty!")
        return self._refresh 
    
    # a setter function 
    @refresh.setter 
    def refresh(self, a): 
        logger.debug("Setting Refresh Token") 
        self._refresh = self.__save_session_token(a, type="refresh")
    
    # Save session token
    def __save_session_token(self, token, type="access"):
        sess_dir = f"{self.home_dir}/{DEFAULT_ECHOME_SESSION_DIR}"

        try:
            if not os.path.exists(sess_dir):
                os.makedirs(sess_dir)
        except Exception as e:
            print("Could not save sessions. Incorrect permissions?")
            raise Exception(e)

        if type == "access":
            fname = "token"
        elif type == "refresh":
            fname = "refresh"
        else:
            raise Exception("Unknown type specified when calling save_session_token")

        token_file = f"{sess_dir}/{fname}"
        with open(token_file, "w") as f:
            f.write(token)
        
        return token
        
    # Get token
    def __get_session(self, type="access"):
        sess_dir = f"{self.home_dir}/{DEFAULT_ECHOME_SESSION_DIR}"

        if type == "access":
            fname = "token"
        elif type == "refresh":
            fname = "refresh"
        else:
            raise Exception("Unknown type specified when calling get_session_token")

        token_file = f"{sess_dir}/{fname}"
        try:
            with open(token_file, "r") as f:
                contents = f.read()
        except:
            return None
        
        return contents

    
    def build_headers(self, token=None):
        header = {
            'user-agent': self.user_agent
        }

        if token:
            header["Authorization"] = f"Bearer {token}"
        
        return header

    # Grab a 
    def __get_local_config(self, config_name):
        
        if self._config_contents is None:
            logger.info("Config file has not yet been parsed, grabbing contents")
            self._config_contents = self.__parse_file(self.conf_file, self.current_profile)
        
        try:
            return self._config_contents[config_name]
        except: 
            logger.info(f"Could not retrieve specified config parameter: '{config_name}'.")
            return ""
        

    def __get_local_credentials(self, credential_name):

        if self._cred_contents is None:
            logger.info("Credentials file has not yet been parsed, grabbing contents")
            self._cred_contents = self.__parse_file(self.cred_file, self.current_profile)

        try:
            return self._cred_contents[credential_name]
        except: 
            logger.info(f"Could not retrieve specified credentials parameter {credential_name}.")
            return ""
    
    def client(self, type):
        """
        Return an API client for the requested type. e.g. .client("vm")
        
        It also supplies this Session with the login to the returned class.
        """
        requested_client = getattr(sys.modules[__name__], type)
        return requested_client(self)
    

    def __parse_file(self, file:str, profile:str):
        """
        Uses ConfigParser to read a provided file. 

        This function, given a profile name (The string in brackets in the file e.g. ["my-profile"])
        will return a dictionary of the items inside of it instead of the list tuple
        """
        parser = ConfigParser()
        parser.read(file)
        dict_items = {}

        if (parser.has_section(profile)):
            items = parser.items(profile)

            for item in items:
                dict_items[item[0]] = item[1]
        else:
            logger.info(f"Parsed file {file} does not have items for the specified profile [{profile}].")
            #raise CredentialsFileError(f"Parsed file {file} does not have items for the specified profile [{profile}].")

        return dict_items
    
    def _get(self, first_value, second_value):
        """
        Returns the first value if it has a value, otherwise, returns the second value.
        """
        #if ( isinstance(first_value, str) and first_value.strip() != "" ):
        if first_value is not None:
            if isinstance(first_value, str) and first_value.strip() == "":
                return second_value
            else:
                return first_value

        return second_value
    

class CredentialsFileError(Exception):
    pass

class ConfigFileError(Exception):
    pass
