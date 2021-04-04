import requests
import logging
import base64
import json
import string
from .response import Response
from .resource import base_resource

class Network(base_resource):
    namespace = "network"

    def describe_all(self, json_response=True):
        r = self.request_url("/describe/all")
        self.status_code = r.status_code
        self.raw_json_response = r.json()
        return r.json()
    
    def describe(self, vnet_id: string, json_response=True):
        r = self.request_url(f"/describe/{vnet_id}")
        self.status_code = r.status_code
        self.raw_json_response = r.json()
        return r.json()
    
    def create(self, vnet_id: string, json_response=True):
        r = self.request_url(f"/create", "post")
        self.status_code = r.status_code
        self.raw_json_response = r.json()
        return r.json()
    
    def delete(self, vnet_id: string, json_response=True):
        r = self.request_url(f"/delete/{vnet_id}", "post")
        self.status_code = r.status_code
        self.raw_json_response = r.json()
        return r.json()
