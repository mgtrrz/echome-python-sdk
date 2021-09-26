import logging
import requests
import platform
import os
import sys
from enum import Enum, auto
from configparser import ConfigParser
from pathlib import Path
from .exceptions import UnrecoverableError, UnauthorizedResponse
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
class Config:
    _credential_contents = {}
    _config_contents = {}

    _access_token:str = None
    _refresh_token:str = None

    class TokenType(Enum):
        ACCESS = "access"
        REFRESH = "refresh"

        def __str__(self) -> str:
            return self.value

    @property
    def access_token(self): 
        logger.debug("Getting Access Token..") 
        if self._access_token is None:
            logger.debug("Session _access_token is empty, attempting to retrieve from local file.")
            self._access_token = self.__retrieve_token(self.TokenType.ACCESS)

        if self._access_token is None:
            logger.debug("Session _access_token is still empty!")
        return self._access_token 
    
    @access_token.setter 
    def access_token(self, value:str) -> None: 
        logger.debug("Setting Access Token") 
        self.__save_token(value, self.TokenType.ACCESS)
        self._access_token = value
    

    @property
    def refresh_token(self): 
        logger.debug("Getting Refresh Token..") 
        if self._refresh_token is None:
            logger.debug("Refresh _token is empty, attempting to retrieve from local file.")
            self._refresh_token = self.__retrieve_token(self.TokenType.REFRESH)

        if self._refresh_token is None:
            logger.debug("Refresh _token is still empty!")
        return self._refresh_token 
    
    @refresh_token.setter 
    def refresh_token(self, value): 
        logger.debug("Setting Refresh Token") 
        self.__save_token(value, self.TokenType.REFRESH)
        self._refresh_token = value
    

    def __save_token(self, value: str, token_type: TokenType) -> None:
        """Save the token value to the temporary session files"""
        sess_dir = f"{str(Path.home())}/{DEFAULT_ECHOME_SESSION_DIR}"

        try:
            if not os.path.exists(sess_dir):
                os.makedirs(sess_dir)
        except Exception as e:
            logger.error("Could not save sessions. Incorrect permissions?")
            raise Exception(e)

        token_file = f"{sess_dir}/{str(token_type)}"
        with open(token_file, "w") as f:
            f.write(value)

        
    def __retrieve_token(self, type:TokenType):
        """Get the token value from the temporary session files"""
        sess_dir = f"{str(Path.home())}/{DEFAULT_ECHOME_SESSION_DIR}"

        token_file = f"{sess_dir}/{str(type)}"
        try:
            with open(token_file, "r") as f:
                contents = f.read()
        except:
            return None
        
        return contents


    def config_value(self, config_key, profile):
        """Will return a value from the config file with a provided key and profile."""
        contents = self.__parse_config_file(profile)
        
        try:
            return contents[config_key]
        except: 
            logger.info(f"Could not retrieve specified config parameter: '{config_key}'.")
            return ""
        

    def credential_value(self, credential_key, profile):
        """Will return a value from the credentials file with a provided key and profile."""
        contents = self.__parse_credentials_file(profile)
        try:
            return contents[credential_key]
        except: 
            logger.info(f"Could not retrieve specified credentials parameter {credential_key}.")
            return ""


    def __parse_config_file(self, profile:str):
        """Grabs the contents of the config file and caches it."""

        if self._config_contents and profile in self._config_contents:
            return self._config_contents[profile]
        
        echome_dir = f"{str(Path.home())}/{DEFAULT_ECHOME_DIR}"
        conf_file  = f"{echome_dir}/{DEFAULT_CONFIG_FILE}"

        contents = self.__parse_file(conf_file, profile)
        self._config_contents[profile] = contents
        return contents


    def __parse_credentials_file(self, profile:str):
        """Grabs the contents of the credentials file and caches it."""

        if self._credential_contents and profile in self._credential_contents:
            return self._credential_contents[profile]
        
        echome_dir = f"{str(Path.home())}/{DEFAULT_ECHOME_DIR}"
        cred_file  = f"{echome_dir}/{DEFAULT_CREDENTIAL_FILE}"

        contents = self.__parse_file(cred_file, profile)
        self._credential_contents[profile] = contents
        return contents


    def __parse_file(self, file:str, profile:str):
        """
        Generic function. Uses ConfigParser to read a provided file. 

        This function, given a profile name (The string in brackets in the file e.g. ["my-profile"])
        will return a dictionary of the items inside of it instead of the list tuple
        """

        logger.debug(f"Parsing file {file} with profile '{profile}'")

        parser = ConfigParser()
        parser.read(file)
        dict_items = {}

        if (parser.has_section(profile)):
            items = parser.items(profile)

            for item in items:
                dict_items[item[0]] = item[1]
        else:
            logger.info(f"Parsed file {file} does not have items for the specified profile [{profile}].")
        return dict_items


class Session:

    config:Config

    def __init__(self, profile:str = None, server:str = None, access_id:str = None, 
            secret_key:str = None, protocol:str = None, login:bool = True):

        # Order of preference for values:
        # If the value is set with in class initiation, these will always take precedence.
        # If no values are supplied, we look for environment variables (ECHOME_PROFILE, ECHOME_SERVER, etc.)
        # If neither are set we look at the user's supplied file for config and credentials.
        self.current_profile = self._get(profile, os.getenv("ECHOME_PROFILE", DEFAULT_PROFILE))
        logger.debug(f"Using profile: {self.current_profile}")

        self.config = Config()
        
        self.server_url = self._get(
            server, 
            os.getenv("ECHOME_SERVER", self.config.config_value("server", self.current_profile))
        )
        self._access_id  = self._get(
            access_id, 
            os.getenv("ECHOME_ACCESS_ID", self.config.credential_value("access_id", self.current_profile))
        )
        self._secret_key = self._get(
            secret_key, 
            os.getenv("ECHOME_SECRET_KEY", self.config.credential_value("secret_key", self.current_profile))
        )
        
        # Some values like 'protocol' will default to the DEFAULT_CONNECTION
        # even if it is not supplied anywhere. 
        proto = self.config.config_value("protocol", self.current_profile) 
        self.connection_type = os.getenv("ECHOME_PROTOCOL", proto if proto else DEFAULT_CONNECTION)

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
        self._load_local_tokens()
        # If the token variable is still empty, log in to set them.
        if login and self.config.access_token is None:
            self.login()
        else:
            logger.debug('login set to false, skipping session grabbing')
    
    def login(self):
        """Login and retrieve tokens from the server"""

        logger.debug("Logging in to ecHome server")
        r = requests.post(
            f"{self.base_url}/identity/token", 
            data={"username": self._access_id, "password": self._secret_key},
            headers=self.build_headers()
        )
        if r.status_code == 200:
            response = r.json()
            self.config.access_token = response["access"]
            self.config.refresh_token = response["refresh"]
            return True
        else:
            raise UnauthorizedResponse("Server did not accept credentials.")
    
    def refresh_access_token(self):
        """Refresh the access token using our refresh token"""
        r = requests.post(
            f"{self.base_url}/identity/token/refresh", 
            headers=self.build_headers(),
            data={"refresh": self.config.refresh_token}
        )
        if r.status_code == 200:
            response = r.json()
            self.config.access_token = response["access"]
            return True
        else:
            raise UnauthorizedResponse("Refresh token no longer valid")
    
    def _load_local_tokens(self):
        self.config.access_token
        self.config.refresh_token
    

    def build_headers(self, token=True):
        header = {
            'user-agent': self.user_agent
        }
        if token:
            header["Authorization"] = f"Bearer {self.config.access_token}"
        return header

    
    def client(self, type):
        """
        Return an API client for the requested type. e.g. .client("vm")
        
        It also supplies this Session with the login to the returned class.
        """
        requested_client = getattr(sys.modules[__name__], type)
        return requested_client(self)
    
    
    def _get(self, first_value, second_value):
        """
        Returns the first value if it has a value, otherwise, returns the second value.
        """
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
