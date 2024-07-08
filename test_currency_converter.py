import unittest
from unittest.mock import patch, Mock
from currency_converter import get_currencies, exchange_rate

class TestCurrencyConverter(unittest.TestCase):

    @patch('currency_converter.get')
    def test_get_currencies_success(self, mock_get):
        mock_response = Mock()
        expected_data = {
            'USD': {'currencyName': 'United States Dollar', 'id': 'USD', 'currencySymbol': '$'},
            'EUR': {'currencyName': 'Euro', 'id': 'EUR', 'currencySymbol': '€'}
        }
        mock_response.json.return_value = {'results': expected_data}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = get_currencies()
        self.assertEqual(result, sorted(list(expected_data.items())))

    @patch('currency_converter.get')
    def test_get_currencies_failure(self, mock_get):
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = Exception("Error")
        mock_get.return_value = mock_response

        with patch('currency_converter.ttk.Text') as MockText:
            mock_text_instance = MockText.return_value
            result = get_currencies(output=mock_text_instance)
            self.assertEqual(result, [])

    @patch('currency_converter.get')
    def test_exchange_rate_success(self, mock_get):
        mock_response = Mock()
        expected_rate = {'USD_EUR': 0.85}
        mock_response.json.return_value = expected_rate
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = exchange_rate('USD', 'EUR')
        self.assertEqual(result, 0.85)

    @patch('currency_converter.get')
    def test_exchange_rate_failure(self, mock_get):
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = Exception("Error")
        mock_get.return_value = mock_response

        with patch('currency_converter.ttk.Text') as MockText:
            mock_text_instance = MockText.return_value
            result = exchange_rate('USD', 'EUR', output=mock_text_instance)
            self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
