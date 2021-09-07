import unittest
import json
from api import calculate_profit
from api.document import crypto_prices
from python.pydantic import ValidationError
class TestCalculateProfit(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.bad_events = [
            {"query":"btc", "amount":100, "year": 2010},
            {"query":"eth", "amount":"hundred", "year": 2010},
            {"amount":"hundred", "year": 2010},
            {"query":"btc", "year": 2010},
            {"query":"eth", "amount":"hundred"},
            {"query": "somestring", "amount":100, "year":2014},
            {"query": "btc", "amount":-40, "year":2014},
            {"query": "btc", "amount":340, "year":445},
            {"query": "btc", "amount":340, "year":"last year"}

        ]

    def test_bad_request_for_invalid_data(self):
        for event in self.bad_events:
            print(event)
            self.assertBadRequest(event)

    def assertBadRequest(self, event):
        try:
            calculate_profit.handler(event, None)
            self.assertFail()
        except Exception as inst:
            assert("[BadRequest]" in str(inst))

    def test_btc_profit_caculation_success(self):
        event = {"query":"btc", "amount":100, "year": 2011}
        expected_result = (event['amount']/crypto_prices[event['query']]['old_prices'][event['year']]) * crypto_prices[event['query']]['current_price']
        result = calculate_profit.handler(event, None)
        self.assertEqual(expected_result, result)

    def test_eth_profit_caculation_success(self):
        event = {"query":"eth", "amount":100, "year": 2016}
        expected_result = (event['amount']/crypto_prices[event['query']]['old_prices'][event['year']]) * crypto_prices[event['query']]['current_price']
        result = calculate_profit.handler(event, None)
        self.assertEqual(expected_result, result)