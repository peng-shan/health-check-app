import unittest
import requests
from unittest.mock import MagicMock, patch
import logging
from health_check import Endpoint, HealthChecker

class EndpointTest(unittest.TestCase):
    def test_check_health_success(self):
        endpoint_data = {
            'name': 'Endpoint 1',
            'url': 'https://www.example.com/',
            'method': 'GET'
        }
        endpoint = Endpoint(**endpoint_data)

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.elapsed.total_seconds.return_value = 0.1

        with patch('requests.request', return_value=mock_response) as mock_request:
            status_code, latency = endpoint.check_health()

            mock_request.assert_called_once_with(
                endpoint.method, endpoint.url, headers=endpoint.headers, json=endpoint.body, timeout=5
            )
            self.assertEqual(status_code, 200)
            self.assertEqual(latency, 100)

    def test_check_health_error(self):
        endpoint_data = {
            'name': 'Endpoint 1',
            'url': 'https://www.example.com/',
            'method': 'GET'
        }
        endpoint = Endpoint(**endpoint_data)

        with patch('requests.request', side_effect=requests.RequestException('Connection error')):
            status_code, latency = endpoint.check_health()

            self.assertIsNone(status_code)
            self.assertIsNone(latency)


class HealthCheckerTest(unittest.TestCase):
    def test_calculate_availability_percentage(self):
        file_path = 'endpoints.yaml'
        health_checker = HealthChecker(file_path)
        health_checker.availability_percentages = {
            'example.com': {'total': 10, 'up': 6},
            'fetchrewards.com': {'total': 5, 'up': 5}
        }

        availability_percentage = health_checker.calculate_availability_percentage('example.com')
        self.assertEqual(availability_percentage, 60)

        availability_percentage = health_checker.calculate_availability_percentage('fetchrewards.com')
        self.assertEqual(availability_percentage, 100)


@patch('logging.info')  # Patch logging.info instead of main.logging.info
@patch('time.sleep', MagicMock())  # Mock time.sleep to avoid actual sleep in the test
@patch('builtins.input', lambda *args: 'endpoints.yaml')
def test_run_health_checks(self, mock_logging):
    file_path = 'endpoints.yaml'
    health_checker = HealthChecker(file_path)
    health_checker.endpoints = [
        MagicMock(spec=Endpoint, name='Endpoint 1'),
        MagicMock(spec=Endpoint, name='Endpoint 2')
    ]

    health_checker.run_health_checks()

    self.assertEqual(mock_logging.call_count, 2)


if __name__ == '__main__':
    unittest.main()
