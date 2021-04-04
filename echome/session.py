import logging
import requests
import base64
import platform
import os
import sys
from configparser import ConfigParser
from os import getenv
from pathlib import Path
from .vm import Vm, Images, SshKey
from .network import Network
from .response import Response
from .network import Network
from .kube import Kube
from .access import Access

default_echome_dir = ".echome"
default_echome_session_dir = ".echome/sess"
default_config_file = "config"
default_credential_file = "credentials"

DEFAULT_PROFILE = "default"

DEFAULT_CONNECTION = "insecure"
DEFAULT_FORMAT = "table"
API_VERSION = "v1"

# Grabs the config and credentials from the user's home dir
# and establishes a connection with the server and authorization
class Session:

    _token = None
    _refresh = None
    _config_contents = None
    _cred_contents = None

    def __init__(self):
        self.home_dir = str(Path.home())
        echome_dir = f"{self.home_dir}/{default_echome_dir}"

        self.cred_file  = f"{echome_dir}/{default_credential_file}"
        self.conf_file  = f"{echome_dir}/{default_config_file}"

        config_from_file = {}

        self.current_profile = getenv("ECHOME_PROFILE", DEFAULT_PROFILE)
        
        self.server_url = getenv("ECHOME_SERVER", self.__get_local_config("server"))
        self.access_id  = getenv("ECHOME_ACCESS_ID", self.__get_local_credentials("access_id"))
        self.secret_key = getenv("ECHOME_SECRET_KEY", self.__get_local_credentials("secret_key"))
        self.connection_type = getenv("ECHOME_PROTOCOL", config_from_file["protocol"] if self.__get_local_config("protocol") else DEFAULT_CONNECTION)
        if self.connection_type == "insecure":
            self.protocol = "http://"
        elif self.connection_type == "secure":
            self.protocol = "https://"
        else:
            raise ConfigFileError(f"Unknown connection type specified. Use either 'secure' or 'insecure'. A blank value defaults to {DEFAULT_CONNECTION}")

        self.format      = getenv("ECHOME_FORMAT", config_from_file["format"] if "format" in config_from_file else DEFAULT_FORMAT)
        self.API_VERSION = API_VERSION

        if not self.server_url:
            Response.unrecoverable_error("ecHome server URL is not set in environment variable or config file. Unable to continue!")
        
        self.base_url = f"{self.protocol}{self.server_url}/{self.API_VERSION}"
        self.user_agent = f"ecHome_sdk/0.2.0 (Python {platform.python_version()}"

        # try retrieving session tokens we already have by reading the files and setting the variables
        self.load_local_tokens()
        # If the token variable is still enpty, log in to set them.
        if self._token is None:
            self.login()

    
    # Login and retrieve a token
    def login(self):
        logging.debug("Logging in to ecHome server")
        r = requests.post(f"{self.base_url}/auth/api/login", auth=(self.access_id, self.secret_key), headers=self.build_headers())
        response = r.json()
        if r.status_code == 200 and "access_token" in response:
            self.token = response["access_token"]
            self.refresh = response["refresh_token"]
            return True
        else:
            return False
    
    # refresh the token
    def refresh_token(self):
        r = requests.post(f"{self.base_url}/auth/api/refresh", headers=self.build_headers(self.refresh))
        response = r.json()
        if r.status_code == 200 and "access_token" in response:
            self.token = response["access_token"]
            return True
        else:
            return False
    
    def load_local_tokens(self):
        self.token
        self.refresh
    
    @property
    def token(self): 
        logging.debug("Getting Token") 
        if self._token is None:
            logging.debug("Session _token is empty, attempting to retrieve from local file.")
            self._token = self.__get_session()

        if self._token is None:
            logging.debug("Session _token is still empty!")
        return self._token 
    
    # a setter function 
    @token.setter 
    def token(self, a): 
        logging.debug("Setting Token") 
        self._token = self.__save_session_token(a)
    

    @property
    def refresh(self): 
        logging.debug("Getting Refresh Token") 
        if self._refresh is None:
            logging.debug("Refresh _token is empty, attempting to retrieve from local file.")
            self._refresh = self.__get_session(type="refresh")

        if self._refresh is None:
            logging.debug("Refresh _token is still empty!")
        return self._refresh 
    
    # a setter function 
    @refresh.setter 
    def refresh(self, a): 
        logging.debug("Setting Refresh Token") 
        self._refresh = self.__save_session_token(a, type="refresh")
    
    # Save session token
    def __save_session_token(self, token, type="access"):
        sess_dir = f"{self.home_dir}/{default_echome_session_dir}"

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
        sess_dir = f"{self.home_dir}/{default_echome_session_dir}"

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

    def __get_local_config(self, config_name):
        
        if self._config_contents is None:
            logging.info("Config file has not yet been parsed, grabbing contents")
            self._config_contents = self.__parse_file(self.conf_file, self.current_profile)
        
        try:
            return self._config_contents[config_name]
        except: 
            logging.info(f"Could not retrieve specified config parameter {config_name}.")
            return ""
        

    def __get_local_credentials(self, credential_name):

        if self._cred_contents is None:
            logging.info("Credentials file has not yet been parsed, grabbing contents")
            self._cred_contents = self.__parse_file(self.cred_file, self.current_profile)

        try:
            return self._cred_contents[credential_name]
        except: 
            logging.info(f"Could not retrieve specified credentials parameter {credential_name}.")
            return ""
    
    def client(self, type):
        """Return an API client for the requested type. e.g. .client("vm")"""
        requested_client = getattr(sys.modules[__name__], type)
        return requested_client(self)
    
    def __parse_file(self, file, profile):
         # profile == ConfigParser's "section" (e.g. [default])
        parser = ConfigParser()
        parser.read(file)
        if (parser.has_section(profile)):
            items = parser.items(profile)

            dict_items = {}
            for item in items:
                dict_items[item[0]] = item[1]
        else:
            logging.info(f"Parsed file {file} does not have items for the specified profile [{profile}].")
            return []
            #raise CredentialsFileError(f"Parsed file {file} does not have items for the specified profile [{profile}].")
        return dict_items

class CredentialsFileError(Exception):
    pass

class ConfigFileError(Exception):
    pass