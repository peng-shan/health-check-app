import logging
import unittest
from unittest import mock
import yaml
from unittest.mock import patch, mock_open
from health_check.health_checker import HealthChecker, Endpoint

class TestHealthChecker(unittest.TestCase):
    @patch('builtins.open', mock_open(read_data=yaml.dump([
        {
            'name': 'Test Endpoint',
            'url': 'http://example.com'
        }
    ])))
    def test_load_endpoints_success(self):
        health_checker = HealthChecker('endpoints.yaml')
        health_checker.load_endpoints()

        self.assertEqual(len(health_checker.endpoints), 1)
        self.assertEqual(health_checker.endpoints[0].name, 'Test Endpoint')
        self.assertEqual(health_checker.endpoints[0].url, 'http://example.com')

    @patch('builtins.open', side_effect=FileNotFoundError())
    def test_load_endpoints_file_not_found(self, mock_open):
        health_checker = HealthChecker('nonexistent.yaml')

        with self.assertRaises(SystemExit):
            health_checker.load_endpoints()

    def test_calculate_availability_percentage(self):
        health_checker = HealthChecker('endpoints.yaml')
        health_checker.availability_percentages = {
            'example.com': {'total': 10, 'up': 7},
            'fetchrewards.com': {'total': 5, 'up': 3}
        }

        availability_percentage = health_checker.calculate_availability_percentage('example.com')
        self.assertEqual(availability_percentage, 70)

        availability_percentage = health_checker.calculate_availability_percentage('fetchrewards.com')
        self.assertEqual(availability_percentage, 60)



    @patch('builtins.open', mock_open(read_data=yaml.dump([
        {
            'name': 'Test Endpoint',
            'url': 'http://example.com'
        }
    ])))
    def test_log_availability_percentages(self):
        # Create a HealthChecker instance and load endpoints
        health_checker = HealthChecker('endpoints.yaml')
        health_checker.load_endpoints()

        # Mock the check_health method of Endpoint to return a specific status code and latency
        with patch.object(Endpoint, 'check_health') as mock_check_health:
            # Mock the first endpoint's check_health method
            mock_check_health.return_value = 200, 300

            # Call the log_availability_percentages method
            health_checker.log_availability_percentages()

            # Verify that the availability percentages are calculated correctly
            availability_percentage = health_checker.calculate_availability_percentage('example.com')
            self.assertEqual(availability_percentage, 100)

            # Reset the mock
            mock_check_health.reset_mock()

            # Mock the first endpoint's check_health method to return different values
            mock_check_health.return_value = 500, 1000

            # Call the log_availability_percentages method again
            health_checker.log_availability_percentages()

            # Verify that the availability percentages are updated correctly
            availability_percentage = health_checker.calculate_availability_percentage('example.com')
            self.assertEqual(availability_percentage, 50)

        # Verify that the total requests count is incremented
        self.assertEqual(health_checker.availability_percentages['example.com']['total'], 2)


if __name__ == '__main__':
    unittest.main()
