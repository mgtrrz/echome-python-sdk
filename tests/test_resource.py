import sys
import os
import unittest
from echome.session import Session
from echome.resource import BaseResource

class BaseResourceTestCase(unittest.TestCase):

    def test_unpack_dict(self):
        base_resource = BaseResource(Session(server="localhost", access_id="1234", secret_key="1234"))
        test_1_dict = {
            "Name": "Resource-1", 
            "Env":"Staging",
            "Automation": True,
            "NoValue": "",
        }
        test_1_result = {
            "Tag": "1",
            "Tag.1.Key": "Name",
            "Tag.1.Value": "Resource-1",
            "Tag.2.Key": "Env", 
            "Tag.2.Value": "Staging",
            "Tag.3.Key": "Automation",
            "Tag.3.Value": True,
            "Tag.4.Key": "NoValue",
            "Tag.4.Value": "",
        }
        self.assertDictEqual(
            base_resource.unpack_dict(test_1_dict, "Tag"), 
            test_1_result
        )