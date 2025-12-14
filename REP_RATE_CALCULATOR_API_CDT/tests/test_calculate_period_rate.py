"""
Unit tests for LMD_CALCULATE_EXPIRED_PERIOD Lambda handler.
Tests period rate calculation functionality with mocks.
"""

import unittest
from unittest.mock import patch, MagicMock
from decimal import Decimal
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestCalculatePeriodRateHandler(unittest.TestCase):
    """Unit tests for calculate period rate Lambda handler"""

    @patch('app.LMD_CALCULATE_EXPIRED_PERIOD.handler.FinancialUtil')
    @patch('app.LMD_CALCULATE_EXPIRED_PERIOD.handler.ProxyUtil')
    def test_successful_period_rate_calculation(self, mock_proxy, mock_financial):
        """Test successful period rate calculation with valid parameters"""
        # Arrange
        mock_proxy.create_response.side_effect = lambda code, body: {'statusCode': code, 'body': body}
        mock_financial.calcular_tasa_vencida.return_value = Decimal('0.0123456789')
        
        event = {
            'annual_effective_rate': '0.05',
            'period_frequency': '12'
        }
        
        # Act
        from app.LMD_CALCULATE_EXPIRED_PERIOD.handler import lambda_handler
        result = lambda_handler(event, {})
        
        # Assert
        self.assertEqual(result['statusCode'], 200)
        self.assertIn('calculated_period_rate_decimal', result['body'])
        self.assertIn('calculated_period_rate_percentage', result['body'])
        self.assertEqual(result['body']['period_frequency'], 12)
        mock_financial.calcular_tasa_vencida.assert_called_once_with(Decimal('0.05'), 12)

    @patch('app.LMD_CALCULATE_EXPIRED_PERIOD.handler.ProxyUtil')
    def test_missing_required_parameters(self, mock_proxy):
        """Test error response when required parameters are missing"""
        # Arrange
        mock_proxy.create_response.side_effect = lambda code, body: {'statusCode': code, 'body': body}
        
        # Missing period_frequency
        event = {
            'annual_effective_rate': '0.05'
        }
        
        # Act
        from app.LMD_CALCULATE_EXPIRED_PERIOD.handler import lambda_handler
        result = lambda_handler(event, {})
        
        # Assert
        self.assertEqual(result['statusCode'], 400)
        self.assertIn('error', result['body'])
        self.assertIn('Missing required parameters', result['body']['error'])

    @patch('app.LMD_CALCULATE_EXPIRED_PERIOD.handler.ProxyUtil')
    def test_invalid_parameter_format(self, mock_proxy):
        """Test error response when parameters have invalid format"""
        # Arrange
        mock_proxy.create_response.side_effect = lambda code, body: {'statusCode': code, 'body': body}
        
        event = {
            'annual_effective_rate': 'not_a_number',
            'period_frequency': '12'
        }
        
        # Act
        from app.LMD_CALCULATE_EXPIRED_PERIOD.handler import lambda_handler
        result = lambda_handler(event, {})
        
        # Assert
        self.assertEqual(result['statusCode'], 400)
        self.assertIn('error', result['body'])
        self.assertIn('Error in parameter format', result['body']['error'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
