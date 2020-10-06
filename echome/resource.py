import requests
import logging
import base64
import json
from .response import Response

class base_resource:
    namespace = ""

    def __init__(self, session, item_id=None):
        self.init_session(session)
    
    def init_session(self, session, namespace=""):
        if namespace:
            self.namespace = namespace
        self.base_url = f"{session.base_url}/{self.namespace}"
        self.session = session
    
    def build_headers(self, type="access"):

        logging.debug("Preparing Requests headers for normal access request")
        headers = {
            'user-agent': self.session.user_agent,
            'Authorization': f"Bearer {self.session.token}"
        }
        
        return headers
    
    def request_url(self, url_namespace, method="get", **kwargs):
        # method here defines the request type to make. 'get' == requests.get, 'post', requests.post, etc.
        try_refresh = False
        try_login = False
        x = 0
        while True:
            logging.debug(f"Calling: {self.base_url}{url_namespace}")
            response = getattr(requests, method)(f"{self.base_url}{url_namespace}", headers=self.build_headers(), params=kwargs)
            logging.debug(f"Got response code: {response.status_code}")

            if response.status_code == 401:
                # Try refreshing the token
                logging.debug("Access token has expired, attempting refresh")
                if self.session.refresh_token() and try_refresh is False:
                    # The method returned True, it should be good to retry.
                    try_refresh = True
                    pass
                else:
                    # If we can't refresh, the refresh token is expired, try logging in to get new token/refresh.
                    if self.session.login() and try_login is False:
                        # try the original call again
                        try_login = True
                        pass
                    else:
                        logging.debug("Unable to login, giving up at this point.")
                        Response.unauthorized_response("Unable to successfully authorize with ecHome server.", exit=True)

            if response.status_code != 401:
                break

            if x > 5:
                logging.warn("While True loop for making a request exceeded 5 loops. This should not have happened.")
                raise Exception("Reached an infinite loop state while making a request that should not have happened. Exiting for safety.")
            x += 1
        
        # Try to unpack the JSON response to see if it's a valid response
        try:
            dec = response.json()
        except json.decoder.JSONDecodeError as e:
            logging.warning("Got non-json response from server.")
            logging.debug(e)
            logging.debug(response.raw.msg)

        
        if response.status_code == 200 or response.status_code == 400 or response.status_code == 404 or response.status_code == 500:
            return response
        else:
            logging.debug(f"Unexpected response from the server: {response.status_code}")
            Response.unexpected_response(f"Unexpected response from the server: {response.raw}", exit=True)

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
