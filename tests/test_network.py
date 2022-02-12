from echome.exceptions import ResourceDoesNotExistError
import unittest
from echome.session import Session
from echome.network import Network
import json
import requests_mock
 
@requests_mock.Mocker()
class NetworkTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.session = Session(server="localhost", access_id="1234", secret_key="1234", login=False)
        self.network_client:Network = Network(self.session)


    def test_network_describe_all_networks(self, mock):
        with open("./tests/responses/network-vnet-describe-all.json") as f:
            file = f.read()
        mock.get('http://localhost/api/v1/network/vent/describe/all', text=file)
        
        self.assertDictEqual(json.loads(file), self.network_client.describe_all_networks())
    

    def test_network_describe_network(self, mock):
        with open("./tests/responses/network-vnet-describe-networks.json") as f:
            file = f.read()
        mock.get('http://localhost/api/v1/network/vent/describe/new-key-test', text=file)

        self.assertDictEqual(json.loads(file), self.network_client.describe_network("new-key-test"))

        with open("./tests/responses/404-response.json") as f:
            file = f.read()
        mock.get('http://localhost/api/v1/network/vent/describe/nokeyhere', text=file, status_code=404)
        
        with self.assertRaises(ResourceDoesNotExistError):
            self.network_client.delete_network("nonetworkhere")
        
 
if __name__ == '__main__':
    NetworkTestCase.main()
