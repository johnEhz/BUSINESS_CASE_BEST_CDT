"""
Integration tests for calculate ROI Lambda handler with real database connection.
These tests use the actual MySQL database and verify real calculations.
"""

import unittest
import sys
import os
from decimal import Decimal
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the parent directory to sys.path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.LMD_CALCULATE_ROI_INTEREST.handler import lambda_handler
from shared.database.db_config import get_db_connection


@unittest.skipUnless(os.getenv("RUN_DB_TESTS") == "1", "Skip DB integration tests (set RUN_DB_TESTS=1 to enable)")
class TestCalculateROIIntegration(unittest.TestCase):
    """Integration tests for calculate ROI with real database"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test data in database before running tests"""
        print("\n=== Setting up test data in database ===")
        
        # First, let's check if there are existing rates in the database
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) as count FROM rates")
                result = cursor.fetchone()
                cls.existing_rates_count = result['count']
                print(f"Existing rates in database: {cls.existing_rates_count}")
                
                # Get sample rates for testing
                cursor.execute("""
                    SELECT consecutive, id_bank, quota, min_term, max_term, min_amount, max_amount 
                    FROM rates 
                    LIMIT 5
                """)
                cls.sample_rates = cursor.fetchall()
                print(f"Sample rates: {cls.sample_rates}")
    
    def test_calculate_roi_with_real_db_existing_rates(self):
        """Test ROI calculation using existing rates from database"""
        if self.existing_rates_count == 0:
            self.skipTest("No rates available in database")
        
        # Use parameters that should match existing rates
        # Typical CDT: 90 days term, $5,000,000 amount
        event = {
            'amount': '5000000',
            'term_in_days': '90',
            'base_days_in_year': 360
        }
        
        result = lambda_handler(event, {})
        
        print(f"\n=== Test Results ===")
        print(f"Status Code: {result['statusCode']}")
        
        # Parse the JSON body
        import json
        body = json.loads(result['body']) if isinstance(result['body'], str) else result['body']
        print(f"Response Body: {body}")
        
        # Assertions
        self.assertEqual(result['statusCode'], 200)
        self.assertIn('investment_summary', body)
        self.assertIn('bank_roi_results', body)
        
        # Verify investment summary
        summary = body['investment_summary']
        self.assertEqual(summary['amount'], '5000000')
        self.assertEqual(summary['term_days'], 90)
        self.assertEqual(summary['base_days_in_year'], 360)
        
        # Print results for manual verification
        bank_results = body['bank_roi_results']
        print(f"\nFound {len(bank_results)} banks matching criteria:")
        for i, bank in enumerate(bank_results, 1):
            print(f"\nBank {i}:")
            print(f"  ID Bank: {bank.get('id_bank')}")
            print(f"  Quota: {bank.get('quota')}%")
            print(f"  Term Range: {bank.get('min_term')}-{bank.get('max_term')} days")
            print(f"  Amount Range: ${bank.get('min_amount'):,.0f} - ${bank.get('max_amount'):,.0f}")
            print(f"  Calculated Interest: ${bank.get('calculated_interest')}")
    
    def test_calculate_roi_with_specific_range(self):
        """Test ROI calculation with specific parameters"""
        if self.existing_rates_count == 0:
            self.skipTest("No rates available in database")
        
        # Test with 180 days (6 months) and $10,000,000
        event = {
            'amount': '10000000',
            'term_in_days': '180',
            'base_days_in_year': 365
        }
        
        result = lambda_handler(event, {})
        
        print(f"\n=== Test 180 days / $10M ===")
        print(f"Status Code: {result['statusCode']}")
        
        self.assertEqual(result['statusCode'], 200)
        
        import json
        body = json.loads(result['body']) if isinstance(result['body'], str) else result['body']
        bank_results = body['bank_roi_results']
        print(f"Found {len(bank_results)} banks for 180 days / $10,000,000")
        
        # Verify that we got results and that interest is calculated
        self.assertGreater(len(bank_results), 0, "Should find at least one bank for these parameters")
        
        # Verify interest calculation for first few banks
        for i, bank in enumerate(bank_results[:3], 1):
            quota = bank['quota']
            calculated_interest = Decimal(bank['calculated_interest'])
            
            print(f"\nBank {bank.get('id_bank')}: quota={quota}%")
            print(f"  Calculated Interest: ${calculated_interest:,.2f}")
            
            # Interest should be positive
            # Note: With compound interest formula, interest can be substantial
            self.assertGreater(calculated_interest, 0, f"Interest should be positive for bank {bank.get('id_bank')}")
            self.assertGreater(calculated_interest, Decimal('10000'), f"Interest seems too low for bank {bank.get('id_bank')}")
    
    def test_calculate_roi_no_matching_rates(self):
        """Test ROI calculation when no rates match the criteria"""
        # Use parameters that likely won't match any rate
        # Very short term and very small amount
        event = {
            'amount': '100',
            'term_in_days': '1',
            'base_days_in_year': 360
        }
        
        result = lambda_handler(event, {})
        
        print(f"\n=== Test No Matching Rates ===")
        print(f"Status Code: {result['statusCode']}")
        
        import json
        body = json.loads(result['body']) if isinstance(result['body'], str) else result['body']
        print(f"Bank Results: {body['bank_roi_results']}")
        
        self.assertEqual(result['statusCode'], 200)
        # Might have empty results or few results
        bank_results = body['bank_roi_results']
        print(f"Found {len(bank_results)} banks for $100 / 1 day")
    
    def test_calculate_roi_with_body_wrapper(self):
        """Test ROI calculation with API Gateway event format (body wrapper)"""
        if self.existing_rates_count == 0:
            self.skipTest("No rates available in database")
        
        import json
        
        # Simulate API Gateway event format
        event = {
            'body': json.dumps({
                'amount': '2000000',
                'term_in_days': '365',
                'base_days_in_year': 360
            })
        }
        
        result = lambda_handler(event, {})
        
        print(f"\n=== Test with Body Wrapper ===")
        print(f"Status Code: {result['statusCode']}")
        
        self.assertEqual(result['statusCode'], 200)
        
        import json
        body = json.loads(result['body']) if isinstance(result['body'], str) else result['body']
        summary = body['investment_summary']
        self.assertEqual(summary['amount'], '2000000')
        self.assertEqual(summary['term_days'], 365)
        
        bank_results = body['bank_roi_results']
        print(f"Found {len(bank_results)} banks for $2M / 365 days")
    
    def test_verify_database_connection(self):
        """Test that database connection is working"""
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT VERSION() as version")
                result = cursor.fetchone()
                print(f"\n=== Database Info ===")
                print(f"MySQL Version: {result['version']}")
                
                cursor.execute("SELECT DATABASE() as db")
                result = cursor.fetchone()
                print(f"Current Database: {result['db']}")
                
                cursor.execute("""
                    SELECT COUNT(*) as rate_count, 
                           MIN(quota) as min_quota, 
                           MAX(quota) as max_quota
                    FROM rates
                """)
                result = cursor.fetchone()
                print(f"Total Rates: {result['rate_count']}")
                print(f"Quota Range: {result['min_quota']}% - {result['max_quota']}%")
        
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main(verbosity=2)
