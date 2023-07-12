import unittest
import requests
from unittest.mock import patch
from health_check.endpoint import Endpoint


class TestEndpoint(unittest.TestCase):
    def test_check_health_success(self):
        # Create an instance of Endpoint
        endpoint = Endpoint(
            name='Test Endpoint',
            url='http://example.com',
            method='GET',
            headers={'User-Agent': 'TestAgent'}
        )

        # Mock the requests.request method to return a successful response
        with patch('requests.request') as mock_request:
            mock_response = mock_request.return_value
            mock_response.status_code = 200
            mock_response.elapsed.total_seconds.return_value = 0.5

            # Call the check_health method
            status_code, latency = endpoint.check_health()

            # Assert that the correct values are returned
            self.assertEqual(status_code, 200)
            self.assertEqual(latency, 500)

            # Assert that requests.request is called with the correct arguments
            mock_request.assert_called_once_with(
                'GET',
                'http://example.com',
                headers={'User-Agent': 'TestAgent'},
                json=None,
                timeout=5
            )

    def test_check_health_failure(self):
        # Create an instance of Endpoint
        endpoint = Endpoint(
            name='Test Endpoint',
            url='http://example.com',
            method='GET',
            headers={'User-Agent': 'TestAgent'}
        )

        # Mock the requests.request method to raise an exception
        with patch('requests.request') as mock_request:
            mock_request.side_effect = requests.RequestException(
                "Request failed")

            # Call the check_health method
            status_code, latency = endpoint.check_health()

            # Assert that None values are returned
            self.assertIsNone(status_code)
            self.assertIsNone(latency)


if __name__ == '__main__':
    unittest.main()
