from echome.exceptions import ResourceDoesNotExistError
import logging
import unittest
from echome.session import Session
from echome.kube import Kube
import json
import requests_mock
 
@requests_mock.Mocker()
class KubeTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.session = Session(server="localhost", access_id="1234", secret_key="1234", login=False)
        self.kube_client = Kube(self.session)


    def test_kube_describe_all(self, mock):
        with open("./tests/responses/kube-describe-all.json") as f:
            file = f.read()
            mock.get('http://localhost/api/v1/kube/cluster/describe', text=f.read())
        
        self.assertDictEqual(json.loads(file), self.kube_client.describe_all_clusters())
    

    def test_vm_describe(self, mock):
        with open("./tests/responses/vm-describe-vm-a00000b1.json") as f:
            file = f.read()
        mock.get('http://localhost/api/v1/vm/vm/describe/vm-a00000b1', text=file)

        self.assertDictEqual(json.loads(file), self.vm_client.describe_vm("vm-a00000b1"))

        with open("./tests/responses/404-response.json") as f:
            file = f.read()
        mock.get('http://localhost/api/v1/vm/vm/describe/vm-a001', text=file, status_code=404)
        
        with self.assertRaises(ResourceDoesNotExistError):
            self.vm_client.describe_vm("vm-a001")
    

    def test_image_guest_describe_all(self, mock):
        with open("./tests/responses/vm-image-guest-all.json") as f:
            file = f.read()
        mock.get('http://localhost/api/v1/vm/image/guest/describe/all', text=file)
        
        self.assertDictEqual(json.loads(file), self.vm_client.describe_all_guest_images())
    

    def test_image_guest_describe(self, mock):
        with open("./tests/responses/vm-image-guest-af2efb3c.json") as f:
            file = f.read()
        mock.get('http://localhost/api/v1/vm/image/guest/describe/gmi-af2efb3c', text=file)

        self.assertDictEqual(json.loads(file), self.vm_client.describe_guest_image("gmi-af2efb3c"))

        with open("./tests/responses/404-response.json") as f:
            file = f.read()
        mock.get('http://localhost/api/v1/vm/image/guest/describe/gmi-a001', text=file, status_code=404)
        
        with self.assertRaises(ResourceDoesNotExistError):
            self.vm_client.describe_guest_image("gmi-a001")
 
 
if __name__ == '__main__':
    VmTestCase.main()
