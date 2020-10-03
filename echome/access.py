import requests
import logging
import base64
import json
import string
from .response import Response
from .resource import base_resource

class Access(base_resource):
    namespace = "access"

    def describe_all(self, json_response=True):
        r = self.request_url("/describe/all")
        self.status_code = r.status_code
        self.raw_json_response = r.json()
        return r.json()
    
    def describe_user(self, user_id: string, json_response=True):
        r = self.request_url(f"/describe/{user_id}")
        self.status_code = r.status_code
        self.raw_json_response = r.json()
        return r.json()
    
    def describe_caller(self, json_response=True):
        r = self.request_url(f"/describe/caller")
        self.status_code = r.status_code
        self.raw_json_response = r.json()
        return r.json()
    
    def create(self, user_id: string, json_response=True):
        r = self.request_url(f"/create", "post")
        self.status_code = r.status_code
        self.raw_json_response = r.json()
        return r.json()
    
    def terminate(self, user_id: string, json_response=True):
        r = self.request_url(f"/terminate/{user_id}", "post")
        self.status_code = r.status_code
        self.raw_json_response = r.json()
        return r.json()
