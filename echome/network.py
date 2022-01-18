import logging
from .resource import BaseResource

logger = logging.getLogger(__name__)

class Network(BaseResource):
    namespace = "network/vnet"

    def describe_all_networks(self):
        return self.get("/network/describe/all")
    
    def describe_network(self, vnet_id:str):
        return self.get(f"/network/describe/{vnet_id}")
    
    def create_network(self):
        return self.post(f"/network/create")
    
    def delete_network(self, vnet_id:str):
        return self.post(f"/network/delete/{vnet_id}")
