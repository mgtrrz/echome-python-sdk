import logging
import unittest
from echome.session import Session, ConfigFileError
 
class SessionTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.session = Session(server="localhost", access_id="1234", secret_key="1234", login=False)

    def test_get(self):
        self.assertEqual("test", self.session._get("test", "second_test"))
        self.assertEqual("second_test", self.session._get(None, "second_test"))
        self.assertEqual("second_test", self.session._get("", "second_test"))
 
 
if __name__ == '__main__':
    SessionTestCase.main()
