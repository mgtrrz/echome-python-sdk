import logging
from .resource import BaseResource

logger = logging.getLogger(__name__)

class Identity(BaseResource):
    namespace = "identity/user"

    def describe_all_users(self):
        return self.request_url("/describe/all")
    
    def describe_user(self, user_id:str):
        return self.request_url(f"/describe/{user_id}")
    
    def describe_caller(self):
        return self.request_url(f"/describe/caller")
    
    def create_user(self, **kwargs):
        if "Tags" in kwargs:
            kwargs.update(self.unpack_tags(kwargs["Tags"]))
        return self.request_url(f"/create", "post", **kwargs)
    
    def delete_user(self, user_id:str):
        return self.request_url(f"/delete/{user_id}", "post")
