import logging
from .resource import BaseResource

logger = logging.getLogger(__name__)

class Images (BaseResource):
    class __guest (BaseResource):
        namespace = "images/guest"

        def describe_all(self):
            return self.request_url(f"/describe/all")

        def describe(self, id):
            return self.request_url(f"/describe/{id}")

        def register(self, **kwargs):
            return self.request_url(f"/register", method="post", **kwargs)
    

    class __user (BaseResource):
        namespace = "images/user"

        def describe_all(self):
            return self.request_url(f"/describe-all")
    
    def guest(self):
        return self.__guest(self.session)

    def user(self):
        return self.__user(self.session)
