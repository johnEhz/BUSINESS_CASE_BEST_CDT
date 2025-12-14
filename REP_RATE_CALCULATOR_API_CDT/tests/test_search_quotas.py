"""
Unit tests for LMD_SEARCH_QUOTAS Lambda handler.
Tests bank quotas search functionality with mocks.
"""

import unittest
from unittest.mock import patch, MagicMock
from decimal import Decimal
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestSearchQuotasHandler(unittest.TestCase):
    """Unit tests for search quotas Lambda handler"""

    @patch('app.LMD_SEARCH_QUOTAS.handler.ProxyUtil')
    @patch('app.LMD_SEARCH_QUOTAS.handler.rates_repo')
    def test_successful_quotas_search(self, mock_repo, mock_proxy):
        """Test successful bank quotas search with valid parameters"""
        # Arrange
        mock_proxy.create_response.side_effect = lambda code, body: {'statusCode': code, 'body': body}
        mock_repo.get_rates_by_terms_and_amount.return_value = [
            {
                'consecutive': 1,
                'id_bank': 1,
                'quota': Decimal('2.1'),
                'min_term': 90,
                'max_term': 119,
                'min_amount': 300000,
                'max_amount': 30000000,
                'last_update': '2021-11-10'
            },
            {
                'consecutive': 2,
                'id_bank': 2,
                'quota': Decimal('2.75'),
                'min_term': 90,
                'max_term': 179,
                'min_amount': 300000,
                'max_amount': 10000000000,
                'last_update': '2021-11-10'
            }
        ]
        
        event = {
            'amount': '5000000',
            'term_in_days': '90'
        }
        
        # Act
        from app.LMD_SEARCH_QUOTAS.handler import lambda_handler
        result = lambda_handler(event, {})
        
        # Assert
        self.assertEqual(result['statusCode'], 200)
        self.assertIn('investment_summary', result['body'])
        self.assertIn('bank_rates', result['body'])
        self.assertEqual(len(result['body']['bank_rates']), 2)
        self.assertEqual(result['body']['investment_summary']['amount'], '5000000')
        self.assertEqual(result['body']['investment_summary']['term_days'], 90)
        mock_repo.get_rates_by_terms_and_amount.assert_called_once_with(90, 5000000.0)

    @patch('app.LMD_SEARCH_QUOTAS.handler.ProxyUtil')
    def test_missing_required_parameters(self, mock_proxy):
        """Test error response when required parameters are missing"""
        # Arrange
        mock_proxy.create_response.side_effect = lambda code, body: {'statusCode': code, 'body': body}
        
        # Missing term_in_days
        event = {
            'amount': '5000000'
        }
        
        # Act
        from app.LMD_SEARCH_QUOTAS.handler import lambda_handler
        result = lambda_handler(event, {})
        
        # Assert
        self.assertEqual(result['statusCode'], 400)
        self.assertIn('error', result['body'])
        self.assertIn('Missing required parameters', result['body']['error'])

    @patch('app.LMD_SEARCH_QUOTAS.handler.ProxyUtil')
    @patch('app.LMD_SEARCH_QUOTAS.handler.rates_repo')
    def test_negative_values_validation(self, mock_repo, mock_proxy):
        """Test error response when negative values are provided"""
        # Arrange
        mock_proxy.create_response.side_effect = lambda code, body: {'statusCode': code, 'body': body}
        
        event = {
            'amount': '-1000',
            'term_in_days': '90'
        }
        
        # Act
        from app.LMD_SEARCH_QUOTAS.handler import lambda_handler
        result = lambda_handler(event, {})
        
        # Assert
        self.assertEqual(result['statusCode'], 400)
        self.assertIn('error', result['body'])
        self.assertIn('must be positive', result['body']['error'])
        mock_repo.get_rates_by_terms_and_amount.assert_not_called()


if __name__ == '__main__':
    unittest.main(verbosity=2)
