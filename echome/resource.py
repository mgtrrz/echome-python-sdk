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
        
        if response.status_code == 200 or response.status_code == 404:
            return response
        else:
            logging.debug(f"Unexpected response from the server: {response.status_code}")
            Response.unexpected_response(f"Unexpected response from the server: {response.json()}", exit=True)

    def unpack_tags(self, tags: dict):
        tag_dict = {}
        num = 1
        tag_dict["Tags"] = "1"
        for tag_key in tags:
            tag_dict[f"Tag.{num}.Key"] = tag_key
            tag_dict[f"Tag.{num}.Value"] = tags[tag_key]
            num = num + 1
        return tag_dict