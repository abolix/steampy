from unittest import TestCase

from steampy.client import SteamClient, LoginRequired, GameOptions


def load_credentials():
    with open('credentials.pwd', 'r') as f:
        return [Credentials(line.split()[0], line.split()[1], line.split()[2]) for line in f]


class Credentials:
    def __init__(self, login: str, password: str, api_key: str):
        self.login = login
        self.password = password
        self.api_key = api_key


class TestSteamClient(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestSteamClient, self).__init__(*args, **kwargs)
        self.credentials = load_credentials()[0]
        self.steam_guard_file = 'Steamguard'

    def test_login(self):
        client = SteamClient(self.credentials.api_key)
        client.login(self.credentials.login, self.credentials.password, self.steam_guard_file)
        self.assertTrue(client.isLoggedIn)

    def test_get_inventory(self):
        client = SteamClient(self.credentials.api_key)
        client.login(self.credentials.login, self.credentials.password, self.steam_guard_file)
        inventory = client.get_my_inventory(GameOptions.CS)
        self.assertIsNotNone(inventory)

    def test_get_trade_offers_summary(self):
        client = SteamClient(self.credentials.api_key)
        summary = client.get_trade_offers_summary()
        self.assertIsNotNone(summary)

    def test_get_trade_offers(self):
        client = SteamClient(self.credentials.api_key)
        offers = client.get_trade_offers()
        self.assertIsNotNone(offers)

    def test_get_trade_offer(self):
        client = SteamClient(self.credentials.api_key)
        trade_offer_id = '1442685162'
        offer = client.get_trade_offer(trade_offer_id)
        self.assertIsNotNone(offer)

    def test_accept_trade_offer_without_login(self):
        client = SteamClient(self.credentials.api_key)
        self.assertRaises(LoginRequired, client.accept_trade_offer, 'id')

    def test_accept_trade_offer(self):
        client = SteamClient(self.credentials.api_key)
        client.login(self.credentials.login, self.credentials.password, self.steam_guard_file)
        trade_offer_id = '1445475351'
        response_dict = client.accept_trade_offer(trade_offer_id)
        self.assertTrue(response_dict['success'])

    def test_decline_trade_offer(self):
        client = SteamClient(self.credentials.api_key)
        client.login(self.credentials.login, self.credentials.password, self.steam_guard_file)
        trade_offer_id = '1449530707'
        response_dict = client.decline_trade_offer(trade_offer_id)
        self.assertEqual(response_dict['response'], {})

    def test_cancel_trade_offer(self):
        client = SteamClient(self.credentials.api_key)
        client.login(self.credentials.login, self.credentials.password, self.steam_guard_file)
        trade_offer_id = '1450637835'
        response_dict = client.cancel_trade_offer(trade_offer_id)
        self.assertEqual(response_dict['response'], {})

    def test_get_price(self):
        client = SteamClient(self.credentials.api_key)
        item = 'M4A1-S | Cyrex (Factory New)'
        prices = client.fetch_price(item, game=GameOptions.CS)
        self.assertTrue(prices['success'])