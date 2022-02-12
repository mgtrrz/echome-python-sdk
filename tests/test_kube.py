from echome.exceptions import ResourceDoesNotExistError
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

        self.assertDictEqual(json.loads(file), self.kube_client.describe_vm("vm-a00000b1"))

        with open("./tests/responses/404-response.json") as f:
            file = f.read()
        mock.get('http://localhost/api/v1/vm/vm/describe/vm-a001', text=file, status_code=404)
        
        with self.assertRaises(ResourceDoesNotExistError):
            self.vm_client.describe_vm("vm-a001")
 
 
if __name__ == '__main__':
    KubeTestCase.main()
