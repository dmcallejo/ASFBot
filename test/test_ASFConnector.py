import unittest
import ASFConnector
import logging


class PersistenceTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.conn = ASFConnector.ASFConnector('192.168.1.254')

    def test_get_asf_info(self):
        info = self.conn.get_asf_info()
        assert info['Success'] is True

    def test_bot_redeem(self):
        response = self.conn.bot_redeem('1', '006ZE-BNMDE-H4YFE')
        assert response is not None


if __name__ == '__main__':
    unittest.main()