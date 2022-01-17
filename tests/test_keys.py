from echome.exceptions import ResourceDoesNotExistError
import logging
import unittest
from echome.session import Session
from echome.keys import Keys
import json
import requests_mock
 
@requests_mock.Mocker()
class KeysTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.session = Session(server="localhost", access_id="1234", secret_key="1234", login=False)
        self.keys_client:Keys = Keys(self.session)


    def test_keys_describe_all_sshkeys(self, mock):
        with open("./tests/responses/keys-sshkey-describe-all.json") as f:
            file = f.read()
        mock.get('http://localhost/api/v1/keys/sshkey/describe/all', text=file)
        
        self.assertDictEqual(json.loads(file), self.keys_client.describe_all_sshkeys())
    

    def test_keys_describe_sshkeys(self, mock):
        with open("./tests/responses/keys-sshkey-describe-new-key-test.json") as f:
            file = f.read()
        mock.get('http://localhost/api/v1/keys/sshkey/describe/new-key-test', text=file)

        self.assertDictEqual(json.loads(file), self.keys_client.describe_sshkey("new-key-test"))

        with open("./tests/responses/404-response.json") as f:
            file = f.read()
        mock.get('http://localhost/api/v1/keys/sshkey/describe/nokeyhere', text=file, status_code=404)
        
        with self.assertRaises(ResourceDoesNotExistError):
            self.keys_client.describe_sshkey("nokeyhere")
        
    
    # def test_keys_import_sshkey(self, mock):
    #     with open("./tests/responses/keys-sshkey-describe-all.json") as f:
    #         file = f.read()
    #     mock.post('http://localhost/api/v1/keys/sshkey/create', text=file)
        
    #     self.assertDictEqual(json.loads(file), self.keys_client.describe_all_sshkeys())
    


 
if __name__ == '__main__':
    KeysTestCase.main()
