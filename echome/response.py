import sys
import logging

logger = logging.getLogger(__name__)

class Response:
    @staticmethod
    def unexpected_response(msg=None):
        print("\t[Unexpected response from server]")
        if msg:
            print(f"\tAdditional information: {msg}")
    
    @staticmethod
    def unauthorized_response(msg=None):
        print("\t[401 Unauthorized]")
        print("\tUnable to login or authorize with the ecHome server.")
        if msg:
            print(f"\tAdditional information: {msg}")
    
    @staticmethod
    def unrecoverable_error(msg=None):
        print("\t[Unrecoverable error]")
        if msg:
            print(f"\tAdditional information: {msg}")
    