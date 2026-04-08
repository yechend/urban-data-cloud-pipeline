"""
File: test_mastodonquery.py
Author: Yechen Deng
Date: 21/05/2024
Description: This unittest tests the functionalities in mastodonquery.py
"""
import unittest
from unittest.mock import patch
import mastodonquery

class TestAusSocialQuery(unittest.TestCase):

    # Test creating ES query
    def test_create_query(self):
        start_date = "2024-05-20"
        end_date = "2024-05-26"
        expected_query = {
            "query": {
                "range": {
                    "created_at": {
                        "gte": start_date,
                        "lte": end_date,
                        "format": "yyyy-MM-dd"
                    }
                }
            },
            "sort": [{"created_at": {"order": "asc"}}],
            "size": 10000
        }
        query = aussocialquery.create_query(start_date, end_date)
        self.assertEqual(query, expected_query)

    # Test the processing of hits from Elasticsearch
    @patch('aussocialquery.client.search')
    def test_process_hits(self, mock_search):
        mock_hits = {
            'hits': {
                'hits': [
                    {'_source': {
                        'created_at': '2024-05-20T07:00:00',
                        'sentiment': 0.1,
                        'count_airquality': 1,
                        'count_traffic': 2,
                        'count_weather': 3
                    }}
                ]
            }
        }
        mock_search.return_value = mock_hits
        hourly_stats = aussocialquery.process_hits(mock_hits['hits']['hits'])
        expected_stats = {
            '2024-05-20T07': {
                'average_sentiment': 0.1,
                'doc_count': 1,
                'cumulative_airquality': 1,
                'cumulative_traffic': 2,
                'cumulative_weather': 3
            }
        }
        self.assertEqual(hourly_stats, expected_stats)

    # Test the main function to handle exceptions
    def test_main_with_exception(self):

        with patch('aussocialquery.client.search', side_effect=Exception("Test Error")):
            with self.assertLogs('aussocialquery.logging', level='ERROR') as cm:
                aussocialquery.main()
                self.assertIn('An error occurred: Test Error', cm.output[0])

if __name__ == '__main__':
    unittest.main()