import base64
import logging
from .resource import BaseResource

logger = logging.getLogger(__name__)

class Keys (BaseResource):
    namespace = "keys"

    def describe_all_sshkeys(self):
        "Describe all SSH keys."
        return self.get("/sshkey/describe/all")


    def describe_sshkey(self, KeyName):
        "Describe an SSH key."
        return self.get(f"/sshkey/describe/{KeyName}")


    def create_sshkey(self, KeyName):
        """Create a new SSH Key."""
        return self.post("/sshkey/create", Action='new', KeyName=KeyName)


    def delete_sshkey(self, KeyName):
        """Delete an existing SSH key."""
        return self.post(f"/sshkey/delete/{KeyName}")


    def import_sshkey(self, KeyName, PublicKey, Tags:dict = None):
        """Import an existing SSH Key."""
        if Tags:
            Tags = self.unpack_tags(Tags)
        
        base64_bytes = base64.b64encode(PublicKey.encode("utf-8"))
        PublicKey = base64_bytes.decode('utf-8')

        return self.post("/sshkey/create", Action='import', KeyName=KeyName, PublicKey=PublicKey, Tags=Tags)
