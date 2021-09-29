import logging
from .resource import BaseResource

logger = logging.getLogger(__name__)

class Network(BaseResource):
    namespace = "network/vnet"

    def describe_all_networks(self):
        return self.request_url("/describe/all")
    
    def describe_network(self, vnet_id:str):
        return self.request_url(f"/describe/{vnet_id}")
    
    def create_network(self, vnet_id:str):
        return self.request_url(f"/create", "post")
    
    def delete_network(self, vnet_id:str):
        return self.request_url(f"/delete/{vnet_id}", "post")
