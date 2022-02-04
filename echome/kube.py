import logging
from .resource import BaseResource

logger = logging.getLogger(__name__)

class Kube(BaseResource):
    namespace = "kube"

    def describe_all_clusters(self):
        return self.get("/cluster/describe/all")
    
    def describe_cluster(self, name:str = None):
        return self.get(f"/cluster/describe/{name}")
    
    def terminate_cluster(self, name:str = None):
        return self.post(f"/cluster/terminate/{name}")
    
    def create_cluster(self, **kwargs):
        if "Tags" in kwargs and kwargs["Tags"] is not None:
            kwargs.update(self.unpack_tags(kwargs["Tags"]))

        return self.post(f"/cluster/create", **kwargs)

    def get_kube_config(self, name:str = None):
        return self.get(f"/cluster/config/{name}")

    def add_node(self, name:str = None, **kwargs):
        if "Tags" in kwargs and kwargs["Tags"] is not None:
            kwargs.update(self.unpack_tags(kwargs["Tags"]))

        return self.post(f"/cluster/modify/{name}", Action='add-node', **kwargs)
