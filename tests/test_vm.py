from echome.exceptions import ResourceDoesNotExistError
import logging
import unittest
from echome.session import Session
from echome.vm import Vm
import json
import requests_mock
 
@requests_mock.Mocker()
class VmTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.session = Session(server="localhost", access_id="1234", secret_key="1234", login=False)
        self.vm_client = Vm(self.session)

    def test_describe_all(self, mock):
        with open("./tests/responses/vm-describe-all.json") as f:
            file = f.read()
        mock.get('http://localhost/api/v1/vm/describe/all', text=file)
        
        self.assertDictEqual(json.loads(file), self.vm_client.describe_all())
    
    def test_describe(self, mock):
        with open("./tests/responses/vm-describe-vm-a00000b1.json") as f:
            file = f.read()
        mock.get('http://localhost/api/v1/vm/describe/vm-a00000b1', text=file)

        self.assertDictEqual(json.loads(file), self.vm_client.describe("vm-a00000b1"))

        with open("./tests/responses/404-response.json") as f:
            file = f.read()
        mock.get('http://localhost/api/v1/vm/describe/vm-a001', text=file, status_code=404)
        
        with self.assertRaises(ResourceDoesNotExistError):
            self.vm_client.describe("vm-a001")
 
 
if __name__ == '__main__':
    VmTestCase.main()
