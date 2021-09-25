import logging
import unittest
from echome.session import Session
from echome.resource import BaseResource

class BaseResourceTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.session = Session(server="localhost", access_id="1234", secret_key="1234", login=False)
        self.base_resource = BaseResource(self.session)

    def test_unpack_dict(self):
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
            self.base_resource.unpack_dict(test_1_dict, "Tag"), 
            test_1_result
        )
    
    def test_unpack_list(self):
        test_list = ["192.168.10.10", "192.168.10.11", "192.168.10.12"]
        test_1_result = {
            "Node": "1",
            "Node.1.Ip": "192.168.10.10",
            "Node.2.Ip": "192.168.10.11",
            "Node.3.Ip": "192.168.10.12",
        }
        test_2_result = {
            "Ip": "1",
            "Ip.1": "192.168.10.10",
            "Ip.2": "192.168.10.11",
            "Ip.3": "192.168.10.12",
        }

        self.assertDictEqual(
            self.base_resource.unpack_list(test_list, "Node", "Ip"), 
            test_1_result
        )
        self.assertDictEqual(
            self.base_resource.unpack_list(test_list, "Ip"), 
            test_2_result
        )


if __name__ == '__main__':
    BaseResourceTestCase.main()
