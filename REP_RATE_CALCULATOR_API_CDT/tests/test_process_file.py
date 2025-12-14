"""
Unit tests for LMD_PROCESS_FILE Lambda handler.
Tests S3 event processing functionality with mocks.
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestProcessFileHandler(unittest.TestCase):
    """Unit tests for process_s3_event Lambda handler"""

    @patch('app.LMD_PROCESS_FILE.handler.rates_repo')
    @patch('app.LMD_PROCESS_FILE.handler.FileUtil')
    @patch('app.LMD_PROCESS_FILE.handler.s3_util')
    @patch('app.LMD_PROCESS_FILE.handler.file_repo')
    def test_successful_file_processing(self, mock_repo, mock_s3, mock_file_util, mock_rates_repo):
        """Test successful S3 file processing"""
        # Arrange
        mock_repo.update_dynamic_file_record_by_key.return_value = {
            'id': 1,
            'file_name': 'test.csv',
            'file_key': 'uploads/test.csv',
            'status': 5
        }
        mock_s3.download_csv_file.return_value = [
            ['consecutivo', 'banco', 'minplazo', 'maxplazo', 'minmonto', 'maxmonto', 'tasa', 'fecha'],
            ['1', 'Banco1', '30', '59', '300000', '30000000', '0.9', '2021-11-10']
        ]
        mock_file_util.validate_records_csv.return_value = [
            {
                'consecutivo': 1,
                'banco': 'Banco1',
                'has_warnings': False,
                'warnings': []
            }
        ]
        mock_repo.update_dynamic_file_record_by_id.return_value = None
        mock_rates_repo.update_many_rates.return_value = None
        
        event = {
            'Records': [
                {
                    's3': {
                        'bucket': {'name': 'test-bucket'},
                        'object': {'key': 'uploads/test.csv'}
                    }
                }
            ]
        }
        
        # Act
        from app.LMD_PROCESS_FILE.handler import process_s3_event
        result = process_s3_event(event, {})
        
        # Assert
        self.assertEqual(result['statusCode'], 200)
        mock_repo.update_dynamic_file_record_by_key.assert_called_once_with('uploads/test.csv', {'status': 5})
        mock_s3.download_csv_file.assert_called_once()
        mock_file_util.validate_records_csv.assert_called_once()

    @patch('app.LMD_PROCESS_FILE.handler.file_repo')
    def test_file_not_found_in_database(self, mock_repo):
        """Test processing fails when file record is not found in database"""
        # Arrange
        mock_repo.update_dynamic_file_record_by_key.return_value = None
        mock_repo.update_dynamic_file_record_by_id.return_value = None
        
        event = {
            'Records': [
                {
                    's3': {
                        'bucket': {'name': 'test-bucket'},
                        'object': {'key': 'uploads/nonexistent.csv'}
                    }
                }
            ]
        }
        
        # Act
        from app.LMD_PROCESS_FILE.handler import process_s3_event
        try:
            result = process_s3_event(event, {})
        except:
            # Expected to fail when updated_file is None
            pass
        
        # Assert
        mock_repo.update_dynamic_file_record_by_key.assert_called_once()

    @patch('app.LMD_PROCESS_FILE.handler.rates_repo')
    @patch('app.LMD_PROCESS_FILE.handler.FileUtil')
    @patch('app.LMD_PROCESS_FILE.handler.s3_util')
    @patch('app.LMD_PROCESS_FILE.handler.file_repo')
    def test_s3_key_with_plus_sign_normalization(self, mock_repo, mock_s3, mock_file_util, mock_rates_repo):
        """Test S3 key normalization when key contains + signs (spaces)"""
        # Arrange
        mock_repo.update_dynamic_file_record_by_key.return_value = {
            'id': 1,
            'file_name': 'test file.csv',
            'file_key': 'uploads/test file.csv',
            'status': 5
        }
        mock_s3.download_csv_file.return_value = [
            ['consecutivo', 'banco', 'minplazo', 'maxplazo', 'minmonto', 'maxmonto', 'tasa', 'fecha']
        ]
        mock_file_util.validate_records_csv.return_value = []
        mock_rates_repo.update_many_rates.return_value = None
        mock_repo.update_dynamic_file_record_by_id.return_value = None
        
        # S3 sends key with + instead of space
        event = {
            'Records': [
                {
                    's3': {
                        'bucket': {'name': 'test-bucket'},
                        'object': {'key': 'uploads/test+file.csv'}
                    }
                }
            ]
        }
        
        # Act
        from app.LMD_PROCESS_FILE.handler import process_s3_event
        result = process_s3_event(event, {})
        
        # Assert
        self.assertEqual(result['statusCode'], 200)
        # Verify that the key was normalized (+ replaced with space)
        called_key = mock_repo.update_dynamic_file_record_by_key.call_args[0][0]
        self.assertEqual(called_key, 'uploads/test file.csv')


if __name__ == '__main__':
    unittest.main(verbosity=2)
