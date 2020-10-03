import requests
import logging
import base64
import json
import string
from .response import Response
from .resource import base_resource

class Kube(base_resource):
    namespace = "kube"

    def describe_all_clusters(self, json_response=True):
        r = self.request_url("/cluster/describe/all")
        self.status_code = r.status_code
        self.raw_json_response = r.json()
        return r.json()
    
    def describe_cluster(self, cluster_id: string, json_response=True):
        r = self.request_url(f"/cluster/describe/{cluster_id}")
        self.status_code = r.status_code
        self.raw_json_response = r.json()
        return r.json()
    
    def create_cluster(self, json_response=True):
        r = self.request_url(f"/cluster/create")
        self.status_code = r.status_code
        self.raw_json_response = r.json()
        return r.json()
    
    def terminate_cluster(self, cluster_id: string, json_response=True):
        r = self.request_url(f"/cluster/terminate/{cluster_id}", "post")
        self.status_code = r.status_code
        self.raw_json_response = r.json()
        return r.json()
    
    def get_kube_config(self, cluster_id: string, json_response=True):
        r = self.request_url(f"/cluster/config/{cluster_id}", "post")
        self.status_code = r.status_code
        self.raw_json_response = r.json()
        return r.json()
