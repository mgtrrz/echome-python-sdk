import base64
import logging
from .resource import BaseResource

logger = logging.getLogger(__name__)

class Keys (BaseResource):
    namespace = "keys/sshkey"

    def describe_all_sshkeys(self):
        return self.request_url(f"/describe/all")
    
    def describe_sshkey(self, KeyName):
        return self.request_url(f"/describe/{KeyName}")

    def create_sshkey(self, KeyName):
        return self.request_url(f"/create", method="post", KeyName=KeyName)

    def delete_sshkey(self, KeyName):
        return self.request_url(f"/delete/{KeyName}", method="post")
    
    def import_sshkey(self, KeyName, PublicKey):
        args = {
            "KeyName": KeyName,
            "PublicKey": base64.urlsafe_b64encode(PublicKey)
        }
        return self.request_url(f"/import", method="post", params=args)
