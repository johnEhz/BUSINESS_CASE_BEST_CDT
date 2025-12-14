import unittest
from unittest.mock import patch, MagicMock
from decimal import Decimal
import json


class TestCalculateROIHandler(unittest.TestCase):
    
    @patch('app.LMD_CALCULATE_ROI_INTEREST.handler.ProxyUtil.create_response')
    @patch('app.LMD_CALCULATE_ROI_INTEREST.handler.FinancialUtil.calcular_roi')
    @patch('app.LMD_CALCULATE_ROI_INTEREST.handler.rates_repo')
    def test_successful_roi_calculation(self, mock_repo, mock_calc_interest, mock_response):
        # Setup mocks
        mock_repo.get_rates_by_terms_and_amount.return_value = [
            {'bank_name': 'Banco A', 'quota': '5.5', 'min_amount': 1000, 'max_amount': 10000},
            {'bank_name': 'Banco B', 'quota': '6.0', 'min_amount': 1000, 'max_amount': 10000}
        ]
        mock_calc_interest.side_effect = [Decimal('137.50'), Decimal('150.00')]
        mock_response.side_effect = lambda code, body: {'statusCode': code, 'body': body}
        
        # Test event
        event = {
            'body': json.dumps({
                'amount': '5000',
                'term_in_days': '90',
                'base_days_in_year': 365
            })
        }
        
        from app.LMD_CALCULATE_ROI_INTEREST.handler import lambda_handler
        result = lambda_handler(event, {})
        
        # Assertions
        self.assertEqual(result['statusCode'], 200)
        self.assertEqual(result['body']['investment_summary']['amount'], '5000')
        self.assertEqual(result['body']['investment_summary']['term_days'], 90)
        self.assertEqual(len(result['body']['bank_roi_results']), 2)
        self.assertEqual(result['body']['bank_roi_results'][0]['calculated_interest'], '137.50')
        self.assertEqual(result['body']['bank_roi_results'][1]['calculated_interest'], '150.00')
        
        # Verify calls
        mock_repo.get_rates_by_terms_and_amount.assert_called_once_with(90, 5000.0)
        self.assertEqual(mock_calc_interest.call_count, 2)
    
    @patch('app.LMD_CALCULATE_ROI_INTEREST.handler.ProxyUtil.create_response')
    def test_missing_required_parameters(self, mock_response):
        mock_response.side_effect = lambda code, body: {'statusCode': code, 'body': body}
        
        # Missing amount
        event = {'body': json.dumps({'term_in_days': '90'})}
        
        from app.LMD_CALCULATE_ROI_INTEREST.handler import lambda_handler
        result = lambda_handler(event, {})
        
        self.assertEqual(result['statusCode'], 400)
        self.assertIn('Missing required parameters', result['body']['error'])
    
    @patch('app.LMD_CALCULATE_ROI_INTEREST.handler.ProxyUtil.create_response')
    def test_invalid_amount_format(self, mock_response):
        mock_response.side_effect = lambda code, body: {'statusCode': code, 'body': body}
        
        event = {
            'body': json.dumps({
                'amount': 'invalid',
                'term_in_days': '90'
            })
        }
        
        from app.LMD_CALCULATE_ROI_INTEREST.handler import lambda_handler
        result = lambda_handler(event, {})
        
        self.assertEqual(result['statusCode'], 400)
        self.assertIn('Error in parameter format', result['body']['error'])
    
    @patch('app.LMD_CALCULATE_ROI_INTEREST.handler.ProxyUtil.create_response')
    def test_negative_values(self, mock_response):
        mock_response.side_effect = lambda code, body: {'statusCode': code, 'body': body}
        
        event = {
            'body': json.dumps({
                'amount': '-1000',
                'term_in_days': '90'
            })
        }
        
        from app.LMD_CALCULATE_ROI_INTEREST.handler import lambda_handler
        result = lambda_handler(event, {})
        
        self.assertEqual(result['statusCode'], 400)
        self.assertIn('Amounts and term must be positive', result['body']['error'])
    
    @patch('app.LMD_CALCULATE_ROI_INTEREST.handler.ProxyUtil.create_response')
    @patch('app.LMD_CALCULATE_ROI_INTEREST.handler.rates_repo')
    def test_database_error_handling(self, mock_repo, mock_response):
        mock_repo.get_rates_by_terms_and_amount.side_effect = Exception('DB Connection Failed')
        mock_response.side_effect = lambda code, body: {'statusCode': code, 'body': body}
        
        event = {
            'body': json.dumps({
                'amount': '5000',
                'term_in_days': '90'
            })
        }
        
        from app.LMD_CALCULATE_ROI_INTEREST.handler import lambda_handler
        result = lambda_handler(event, {})
        
        self.assertEqual(result['statusCode'], 500)
        self.assertIn('Internal server error', result['body']['error'])
    
    @patch('app.LMD_CALCULATE_ROI_INTEREST.handler.ProxyUtil.create_response')
    @patch('app.LMD_CALCULATE_ROI_INTEREST.handler.rates_repo')
    def test_direct_event_without_body(self, mock_repo, mock_response):
        """Test when event is passed directly without body wrapper"""
        mock_repo.get_rates_by_terms_and_amount.return_value = []
        mock_response.side_effect = lambda code, body: {'statusCode': code, 'body': body}
        
        # Direct event (no 'body' key)
        event = {
            'amount': '5000',
            'term_in_days': '90',
            'base_days_in_year': 360
        }
        
        from app.LMD_CALCULATE_ROI_INTEREST.handler import lambda_handler
        result = lambda_handler(event, {})
        
        self.assertEqual(result['statusCode'], 200)
        self.assertEqual(result['body']['investment_summary']['base_days_in_year'], 360)
        mock_repo.get_rates_by_terms_and_amount.assert_called_once_with(90, 5000.0)


if __name__ == '__main__':
    unittest.main()