import logging
import base64
from .resource import BaseResource

logger = logging.getLogger(__name__)

class Vm (BaseResource):
    namespace = "vm"

    def describe_all_vms(self):
        return self.request_url("/vm/describe/all")

    def describe_vm(self, vm_id):
        return self.request_url(f"/vm/describe/{vm_id}")
        
    def create_vm(self, **kwargs):
        if "Tags" in kwargs and kwargs["Tags"] is not None:
            kwargs.update(self.unpack_tags(kwargs["Tags"]))
        
        if "UserDataScript" in kwargs:
            base64_bytes = base64.b64encode(kwargs["UserDataScript"].encode("utf-8"))
            kwargs["UserDataScript"] = base64_bytes.decode('utf-8')
        
        return self.request_url("/vm/create", "post", **kwargs)
    
    def stop_vm(self, vm_id):
        return self.request_url(f"/vm/modify/{vm_id}", "post", Action='stop')
    
    def start_vm(self, vm_id):
        return self.request_url(f"/vm/modify/{vm_id}", "post", Action='start')

    def terminate_vm(self, vm_id):
        return self.request_url(f"/vm/terminate/{vm_id}", "post")

    def create_vm_image(self, vm_id, **kwargs):
        if "Tags" in kwargs and kwargs["Tags"] is not None:
            kwargs.update(self.unpack_tags(kwargs["Tags"]))
        return self.request_url(f"/vm/modify/{vm_id}", "post", Action='create-image', **kwargs)


    def describe_all_volumes(self):
        return self.request_url("/volume/describe/all")

    def describe_volume(self, vol_id):
        return self.request_url(f"/volume/describe/{vol_id}") 


    def describe_all_guest_images(self):
            return self.request_url(f"/image/guest/describe/all")

    def describe_guest_image(self, id):
        return self.request_url(f"/image/guest/describe/{id}")

    def register_guest_image(self, **kwargs):
        return self.request_url(f"/image/guest/register", method="post", **kwargs)

    def describe_all_user_images(self):
            return self.request_url(f"/image/user/describe/all")

    def describe_user_image(self, id):
        return self.request_url(f"/image/user/describe/{id}")

