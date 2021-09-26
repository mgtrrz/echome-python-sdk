import requests
import base64
import json
import logging
from .resource import BaseResource

logger = logging.getLogger(__name__)

class Vm (BaseResource):
    namespace = "vm"

    def describe_all(self, json_response=True):
        r = self.request_url("/describe/all")
        self.status_code = r.status_code
        self.raw_json_response = r.json()
        return r.json()

    def describe(self, vm_id, json_response=True):
        r = self.request_url(f"/describe/{vm_id}")
        self.status_code = r.status_code
        self.raw_json_response = r.json()

        if r.status_code != 200:
            # TODO: Error handling
            return r.json()

        resp = json.loads(r.text)
        for vm in resp:
            instobj = Instance(
                self.session, 
                self.namespace, 
                attached_interfaces = vm["attached_interfaces"],
                created = vm["created"],
                host = vm["host"],
                instance_id = vm["instance_id"],
                instance_size = f"{vm['instance_type']}.{vm['instance_size']}",
                key_name = vm["key_name"],
                state = vm["state"],
                tags = vm["tags"]
            )
        if not json_response:
            return instobj
        else:
            return resp
    
    def set_metadata(self, **kwargs):
        self.vm_id = kwargs.get("instance_id")
        self.attached_interfaces = kwargs.get("attached_interfaces", "")
        self.host = kwargs.get("host", "")
        self.created = kwargs.get("created", "")
        self.key_name = kwargs.get("key_name", "")
        self.instance_size = kwargs.get('instance_size', "")
        self.state = kwargs.get("state", {})
        self.tags = kwargs.get("tags", {})
        
    def create(self, **kwargs):
        if "Tags" in kwargs and kwargs["Tags"] is not None:
            kwargs.update(self.unpack_tags(kwargs["Tags"]))
        
        r = self.request_url("/create", "post", **kwargs)
        self.status_code = r.status_code
        return r.json()
    
    def stop(self, id=""):
        if not id:
            id = self.vm_id
        
        r = self.request_url(f"/modify/{id}", "post", Action='stop')
        self.status_code = r.status_code
        return r.json()
    
    def start(self, id=""):
        if not id:
            id = self.vm_id

        r = self.request_url(f"/modify/{id}", "post", Action='start')
        self.status_code = r.status_code
        return r.json()

    def terminate(self, id=""):
        if not id:
            id = self.vm_id

        r = self.request_url(f"/terminate/{id}", "post")
        self.status_code = r.status_code
        return r.json()
    
    def __str__(self):
        if self.vm_id:
            return self.vm_id
        else:
            return "GenericVmObject"
        

class Instance (BaseResource):
    def __init__(self, session, namespace, **kwargs):
        self.vm_id = kwargs.get("instance_id")
        self.attached_interfaces = kwargs.get("attached_interfaces", "")
        self.host = kwargs.get("host", "")
        self.created = kwargs.get("created", "")
        self.key_name = kwargs.get("key_name", "")
        self.instance_size = kwargs.get('instance_size', "")
        self.state = kwargs.get("state", {})
        self.tags = kwargs.get("tags", {})

        self.namespace = namespace
        self.init_session(session)
    
    def __str__(self):
        return self.vm_id

# TODO: Return image objects

class Images (BaseResource):
    class __guest (BaseResource):
        namespace = "vm/images/guest"

        def describe_all(self):
            r = self.request_url(f"/describe/all")
            self.status_code = r.status_code
            return r.json()

        def describe(self, id):
            r = self.request_url(f"/describe/{id}")
            self.status_code = r.status_code
            return r.json()

        def register(self, **kwargs):
            r = self.request_url(f"/register", method="post", **kwargs)
            self.status_code = r.status_code
            return r.json()

    
    class __user (BaseResource):
        namespace = "vm/images/user"

        def describe_all(self):
            r = self.request_url(f"/describe-all")
            self.status_code = r.status_code
            return r.json()
    
    def guest(self):
        return self.__guest(self.session)

    def user(self):
        return self.__user(self.session)


class SshKey (BaseResource):
    namespace = "vm/ssh_key"

    def describe_all(self):
        r = self.request_url(f"/describe/all")
        self.status_code = r.status_code
        return r.json()

    
    def describe(self, KeyName):
        r = self.request_url(f"/describe/{KeyName}")
        self.status_code = r.status_code
        return r.json()

    
    def create(self, KeyName):
        r = self.request_url(f"/create", method="post", KeyName=KeyName)
        self.status_code = r.status_code
        return r.json()
    

    def delete(self, KeyName):
        r = self.request_url(f"/delete/{KeyName}", method="post")
        self.status_code = r.status_code
        return r.json()
    

    def import_key(self, KeyName, PublicKey):
        args = {
            "KeyName": KeyName,
            "PublicKey": base64.urlsafe_b64encode(PublicKey)
        }
        r = self.request_url(f"/import", method="post", params=args)
        self.status_code = r.status_code
        return r.json()

class SshKeyObject(BaseResource):

    def __init__(self, session, namespace, **kwargs):
        self.fingerprint = kwargs["fingerprint"]
        self.key_id = kwargs["key_id"]
        self.key_name = kwargs["key_name"]
        self.namespace = namespace
        self.init_session(session)
    
    def __str__(self):
        return self.key_name
    
    def delete(self):
        r = requests.get(f"{self.base_url}/delete/{self.key_name}")
        self.status_code = r.status_code
        return r.json()
