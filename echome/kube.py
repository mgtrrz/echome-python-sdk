import string
import logging
from .resource import BaseResource

logger = logging.getLogger(__name__)

class Kube(BaseResource):
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
    
    def terminate_cluster(self, cluster_id: string, json_response=True):
        r = self.request_url(f"/cluster/terminate/{cluster_id}", "post")
        self.status_code = r.status_code
        self.raw_json_response = r.json()
        return r.json()
    
    def create_cluster(self, **kwargs):
        if "Tags" in kwargs:
            kwargs.update(self.unpack_tags(kwargs["Tags"]))
        
        if "NodeIps" in kwargs and isinstance(kwargs["NodeIps"], list):
            kwargs.update(self.unpack_list(kwargs["NodeIps"], "Node", "Ip"))
        else:
            raise ValueError("NodeIps must be included and of type list.")

        r = self.request_url(f"/cluster/create", "post", **kwargs)
        self.status_code = r.status_code
        self.raw_json_response = r.json()
        return r.json()
    
    def get_kube_config(self, cluster_id: string, json_response=True):
        r = self.request_url(f"/cluster/config/{cluster_id}")
        self.status_code = r.status_code
        self.raw_json_response = r.json()
        return r.json()
