import unittest
from unittest import mock
from health_check.health_checker import HealthChecker

class TestHealthChecker(unittest.TestCase):
    @mock.patch('builtins.open', new_callable=mock.mock_open, read_data="some_data")
    @mock.patch('yaml.safe_load')
    def test_load_endpoints(self, mock_yaml_load, mock_open):
        mock_yaml_load.return_value = [
            {'url': 'http://example.com/endpoint1', 'name': 'Endpoint1'},
            {'url': 'http://example.com/endpoint2', 'name': 'Endpoint2'}
        ]
        hc = HealthChecker('fake_path.yaml')
        hc.load_endpoints()

        mock_open.assert_called_once_with('fake_path.yaml', 'r')
        mock_yaml_load.assert_called_once()
        self.assertEqual(len(hc.endpoints), 2)
        self.assertEqual(hc.domains, {'example.com'})
        self.assertEqual(hc.availability_percentages, {'example.com': {'total': 0, 'up': 0}})

    def test_calculate_availability_percentage(self):
        hc = HealthChecker('fake_path.yaml')
        hc.availability_percentages = {
            'example.com': {
                'total': 100,
                'up': 50
            }
        }
        percentage = hc.calculate_availability_percentage('example.com')
        self.assertEqual(percentage, 50)

    @mock.patch('concurrent.futures.ThreadPoolExecutor')
    def test_send_health_check_requests(self, mock_executor):
        mock_future = mock.Mock()
        mock_executor.return_value.__enter__.return_value.submit.return_value = mock_future
        mock_future.result.return_value = (200, 400)
        mock_endpoint = mock.Mock()
        mock_endpoint.check_health.return_value = (200, 400)
        mock_endpoint.url = 'http://example.com/endpoint1'
        mock_endpoint.name = 'Endpoint1'

        hc = HealthChecker('fake_path.yaml')
        hc.endpoints = [mock_endpoint]
        hc.availability_percentages = {'example.com': {'total': 0, 'up': 0}}

        hc.send_health_check_requests()

        self.assertEqual(hc.availability_percentages, {'example.com': {'total': 1, 'up': 1}})

if __name__ == '__main__':
    unittest.main()
