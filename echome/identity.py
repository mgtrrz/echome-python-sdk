import string
import logging
from .resource import BaseResource

logger = logging.getLogger(__name__)

class Identity(BaseResource):
    namespace = "identity"

    def describe_all(self, json_response=True):
        r = self.request_url("/describe/all")
        self.status_code = r.status_code
        self.raw_json_response = r.json()
        return r.json()
    
    def describe_user(self, user_id: string, json_response=True):
        r = self.request_url(f"/describe/{user_id}")
        self.status_code = r.status_code
        self.raw_json_response = r.json()
        return r.json()
    
    def describe_caller(self, json_response=True):
        r = self.request_url(f"/describe/caller")
        self.status_code = r.status_code
        self.raw_json_response = r.json()
        return r.json()
    
    def create(self, **kwargs):
        if "Tags" in kwargs:
            kwargs.update(self.unpack_tags(kwargs["Tags"]))
        r = self.request_url(f"/create", "post", **kwargs)
        self.status_code = r.status_code
        self.raw_json_response = r.json()
        return r.json()
    
    def delete(self, user_id: string, json_response=True):
        r = self.request_url(f"/delete/{user_id}", "post")
        self.status_code = r.status_code
        self.raw_json_response = r.json()
        return r.json()
