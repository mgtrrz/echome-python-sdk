import logging
from .resource import BaseResource

logger = logging.getLogger(__name__)

class Vm (BaseResource):
    namespace = "vm/vm"

    def describe_all_vms(self):
        return self.request_url("/describe/all")

    def describe_vm(self, vm_id):
        return self.request_url(f"/describe/{vm_id}")
        
    def create_vm(self, **kwargs):
        if "Tags" in kwargs and kwargs["Tags"] is not None:
            kwargs.update(self.unpack_tags(kwargs["Tags"]))
        
        return self.request_url("/create", "post", **kwargs)
    
    def stop_vm(self):
        return self.request_url(f"/modify/{id}", "post", Action='stop')
    
    def start_vm(self, id):
        return self.request_url(f"/modify/{id}", "post", Action='start')

    def terminate_vm(self, id):
        return self.request_url(f"/terminate/{id}", "post")
