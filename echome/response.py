import sys
import logging

logger = logging.getLogger(__name__)

class Response:
    @staticmethod
    def unexpected_response(msg=None, exit=False):
        print("\t[Unexpected response from server]")
        if msg:
            print(f"\tAdditional information: {msg}")
        # if exit:
        #     sys.exit(1)
    
    @staticmethod
    def unauthorized_response(msg=None, exit=False):
        print("\t[401 Unauthorized]")
        print("\tUnable to login or authorize with the ecHome server.")
        if msg:
            print(f"\tAdditional information: {msg}")
        # if exit:
        #     sys.exit(1)
    
    @staticmethod
    def unrecoverable_error(msg=None, exit=True):
        print("\t[Unrecoverable error]")
        if msg:
            print(f"\tAdditional information: {msg}")
        # if exit:
        #     sys.exit(1)
    