import unittest

from rocketreach.gateway import GatewayConfig, GatewayEnvironment, Gateway


class TestAccount(unittest.TestCase):
    def setUp(self) -> None:
        key = Gateway.sandbox_api_key
        config = GatewayConfig(api_key=key, environment=GatewayEnvironment.Development)
        self.gw = Gateway(config)

    def test_account(self):
        account_result = self.gw.account.get()
        self.assertTrue(account_result.is_success)
        self.assertEqual(account_result.account.state, 'test_user')

    def test_search(self):
        s = self.gw.person.search()
        s = s.filter(name='Marc')
        search_result = s.execute()
        self.assertTrue(search_result.is_success)
        self.assertTrue(len(search_result.people) > 0)
