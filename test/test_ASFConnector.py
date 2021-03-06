import unittest
import ASFConnector
import logger


class PersistenceTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logger.set_logger('ASFBotTest')
        cls.conn = ASFConnector.ASFConnector('10.8.0.1')

    def test_get_asf_info(self):
        info = self.conn.get_asf_info()
        assert info['Success'] is True

    def test_bot_redeem(self):
        response = self.conn.bot_redeem('1', '006ZE-BNMDE-H4YFE')
        assert response is not None


if __name__ == '__main__':
    unittest.main()