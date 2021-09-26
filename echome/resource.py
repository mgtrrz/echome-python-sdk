import requests
import logging
import json
from .exceptions import UnauthorizedResponse, UnexpectedResponseError, UnrecoverableError

logger = logging.getLogger(__name__)

class BaseResource:
    namespace = ""

    def __init__(self, session):
        self.init_session(session)
    
    def init_session(self, session, namespace=""):
        if namespace:
            self.namespace = namespace
        self.base_url = f"{session.base_url}/{self.namespace}"
        self.session = session
    
    def build_headers(self):
        headers = {
            'user-agent': self.session.user_agent,
            'Authorization': f"Bearer {self.session.config.access_token}"
        }
        
        return headers
    
    def request_url(self, url_namespace, method="get", **kwargs):
        # method here defines the request type to make. 'get' == requests.get, 'post', requests.post, etc.
        tried_refresh = False
        tried_login = False
        x = 0
        while True:
            logger.debug(f"Calling: {self.base_url}{url_namespace}")
            response = getattr(requests, method)(f"{self.base_url}{url_namespace}", headers=self.build_headers(), data=kwargs)
            logger.debug(f"Got response code: {response.status_code}")

            if response.status_code == 401:
                # We got a 401, try refreshing the access token.
                logger.debug("Access token has expired, attempting refresh")
                try:
                    self.session.refresh_access_token()
                except UnauthorizedResponse:
                    # That still failed, try logging in.
                    logger.debug("401 when refreshing access token, going to try logging in.")
                    try:
                        self.session.login()
                    except UnauthorizedResponse:
                        raise "Unable to successfully authorize with ecHome server."

            if response.status_code != 401:
                break

            if x > 5:
                logger.warn("While True loop for making a request exceeded 5 loops. This should not have happened.")
                raise UnrecoverableError("Reached an infinite loop state while making a request that should not have happened. Exiting for safety.")
            x += 1
        
        # Try to unpack the JSON response to see if it's a valid response
        try:
            dec = response.json()
        except json.decoder.JSONDecodeError as e:
            logger.warning("Got non-json response from server.")
            logger.debug(e)
            logger.debug(response.raw.msg)

        
        if response.status_code in [200, 400, 404]:
            return response
        else:
            logger.debug(f"Unexpected response from the server: {response.status_code}")
            raise UnexpectedResponseError(f"Got unexpected response from the server. Status code: {response.status_code}")

    def unpack_tags(self, tags: dict):
        return self.unpack_dict(tags, "Tag")
    
    # Given a dictionary of tags for a resource, will return a dictionary
    # to make an HTTP request with.
    # e.g. {"Name": "Resource-1", "Env":"Staging"}
    # returns: {
    #     "Tag.1.Key": "Name",
    #     "Tag.1.Value": "Resource-1",
    #     "Tag.2.Key": "Env", 
    #     "Tag.2.Value": "Staging"
    # }
    def unpack_dict(self, generic_dict:dict, dict_name:str):
        unpacked_dict = {}
        num = 1
        unpacked_dict[dict_name] = "1"
        for dict_key in generic_dict:
            unpacked_dict[f"{dict_name}.{num}.Key"] = dict_key
            unpacked_dict[f"{dict_name}.{num}.Value"] = generic_dict[dict_key]
            num += 1
        return unpacked_dict
    
    # Given a generic list, and a name to use for the list, will return a
    # dictionary to make an HTTP request with.
    # e.g. generic_list = ["192.168.10.10", "192.168.10.11", "192.168.10.12"]
    #      list_name = "Node",
    #      list_name_append = "Ip"
    # returns: {
    #     "Node.1.Ip": "192.168.10.10",
    #     "Node.2.Ip": "192.168.10.11",
    #     "Node.3.Ip": "192.168.10.12",
    # }
    # list_name_append is optional, if ommited, the key would simply look like:
    # "Node.1"
    def unpack_list(self, generic_list:list, list_name:str, list_name_append:str=None):
        if list_name_append:
            list_name_append = f".{list_name_append}"
        else:
            list_name_append = ""

        unpacked_dict = {}
        num = 1
        unpacked_dict[list_name] = "1"
        for val in generic_list:
            unpacked_dict[f"{list_name}.{num}{list_name_append}"] = val
            num += 1
        return unpacked_dict
