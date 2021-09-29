import logging
from .resource import BaseResource

logger = logging.getLogger(__name__)

class Kube(BaseResource):
    namespace = "kube"

    def describe_all_clusters(self):
        return self.request_url("/cluster/describe/all")
    
    def describe_cluster(self, cluster_id:str):
        return self.request_url(f"/cluster/describe/{cluster_id}")
    
    def terminate_cluster(self, cluster_id:str):
        return self.request_url(f"/cluster/terminate/{cluster_id}", "post")
    
    def create_cluster(self, **kwargs):
        if "Tags" in kwargs:
            kwargs.update(self.unpack_tags(kwargs["Tags"]))
        
        if "NodeIps" in kwargs and isinstance(kwargs["NodeIps"], list):
            kwargs.update(self.unpack_list(kwargs["NodeIps"], "Node", "Ip"))
        else:
            raise ValueError("NodeIps must be included and of type list.")

        return self.request_url(f"/cluster/create", "post", **kwargs)

    def get_kube_config(self, cluster_id:str):
        return self.request_url(f"/cluster/config/{cluster_id}")

