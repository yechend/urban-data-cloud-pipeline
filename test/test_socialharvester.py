"""
File: test_socialharvester.py
Author: Yechen Deng
Date: 21/05/2024
Description: This unittest tests the seven functionalities in socialharvester.py
"""
import unittest
from socialharvester import remove_html_tags, get_tokens, parse_html,extract_post_info, update_state, read_state
from datetime import datetime
from unittest.mock import patch, MagicMock

class TestSocialHarvester(unittest.TestCase):

    # Test remove the html tags in the conten
    def test_remove_html_tags(self):
        html_content = "<p>Hello, <b>world!</b></p>"
        expected_output = "Hello, world!"
        self.assertEqual(remove_html_tags(html_content), expected_output)

    # Test the NLP processing steps
    def test_get_tokens(self):
        content = "Hello, this is a test!"
        expected_tokens = ['hello', 'test']
        self.assertEqual(get_tokens(content), expected_tokens)

    # Test extracting mention tags
    def test_parse_html(self):
        html = '<p><a class="mention hashtag" href="https://example.com">#Test</a></p>'
        result = parse_html(html)
        self.assertIsNotNone(result)
        self.assertEqual(result.get_text(), '#Test')

    # Test the count calculated in one function in socialharvester
    @patch('socialharvester.requests.get')
    def test_get_timelines(self, mocked_get):
        mocked_get.return_value.status_code = 200
        mocked_get.return_value.json.return_value = [{
            "created_at": "2024-05-20T12:00:00.000Z", "id": "1234", "content": "Test content", "tags": [], "language": "en"
        }]

        from socialharvester import get_timelines  # ensure imported properly to avoid patch issues
        count = get_timelines('token_dummy', 'https://dummy.social', 1, None)
        self.assertEqual(count, 1)
        mocked_get.assert_called_once()

# Set up a test post
def setUp(self):
    self.post_data = {
        "created_at": "2024-05-20T12:00:00.000Z",
        "id": "1234",
        "content": "<p>Hello world! #weather #storm</p>",
        "tags": [{"name": "weather"}, {"name": "storm"}],
        "language": "en"
    }

# Test the main function to extract content
@patch('socialharvester.datetime')
def test_extract_post_info(self, mock_datetime):
    mock_datetime.strptime.return_value = datetime(2024, 5, 20, 12, 0, 0)
    mock_datetime.isoformat.return_value = '2024-05-20T12:00:00.000Z'

    result = extract_post_info(self.post_data)
    self.assertEqual(result['id'], '1234')
    self.assertEqual(result['lang'], 'en')
    self.assertIn('weather', result['tags'])
    self.assertEqual(result['sentiment'], 0)
    self.assertGreater(result['count_weather'], 0)

# Test update the state
@patch('socialharvester.Elasticsearch')
def test_update_state(self, mock_es):
    mock_es.return_value.index.return_value = {'result': 'updated'}
    cumulative_counts = {'cumul_sum_weather': 10, 'cumul_sum_traffic': 5, 'cumul_sum_airquality': 3}
    response = update_state('prefix', 'max_id', 100, cumulative_counts, mock_es.return_value)
    mock_es.return_value.index.assert_called_once()
    self.assertEqual(response['result'], 'updated')

# Test read the previous/current state
@patch('socialharvester.Elasticsearch')
def test_read_state(self, mock_es):
    expected_state = {
        'last_id': '1234',
        'record_count': 10,
        'cumul_sum_weather': 5,
        'cumul_sum_traffic': 3,
        'cumul_sum_airquality': 2
    }
    mock_es.return_value.search.return_value = {
        'timed_out': False,
        'hits': {
            'hits': [
                {'_source': expected_state}
            ]
        }
    }
    record_count, last_id, state = read_state('prefix', mock_es.return_value)
    self.assertEqual(last_id, '1234')
    self.assertEqual(record_count, 10)
    self.assertEqual(state['cumul_sum_weather'], 5)

if __name__ == '__main__':
    unittest.main()