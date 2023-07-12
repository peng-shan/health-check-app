import yaml
import logging
import time
from health_check.endpoint import Endpoint

class HealthChecker:
    def __init__(self, file_path):
        """
        Performs health checks on a set of HTTP endpoints.

        Args:
            file_path (str): The path to the YAML configuration file.
        """
        self.file_path = file_path
        self.endpoints = []
        self.domains = set()
        self.availability_percentages = {}
        self.total_requests = 0
        self.test_cycle_count = 0

        # Configure logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def load_endpoints(self):
        """
        Loads the endpoints from the YAML configuration file.
        """
        try:
            with open(self.file_path, 'r') as file:
                endpoints_data = yaml.safe_load(file)

            for endpoint_data in endpoints_data:
                endpoint = Endpoint(**endpoint_data)
                self.endpoints.append(endpoint)
                domain = endpoint.url.split('/')[2]
                self.domains.add(domain)
                self.availability_percentages[domain] = {'total': 0, 'up': 0}
        except FileNotFoundError:
            logging.error("File not found.")
            raise SystemExit(1)  # Terminate program execution
        except yaml.YAMLError as e:
            logging.error(f"Error parsing YAML file: {e}")
            raise SystemExit(1)  # Terminate program execution

    def calculate_availability_percentage(self, domain):
        """
        Calculates the availability percentage.

        Args:
            domain (str): The domain for which to calculate the availability percentage.

        Returns:
            int: The availability percentage.
        """
        total_count = self.availability_percentages[domain]['total']
        up_count = self.availability_percentages[domain]['up']

        if total_count == 0:
            return 0
        return round((up_count / total_count) * 100)

    def log_availability_percentages(self):
        """
        Logs the availability percentages for each domain.
        """
        self.test_cycle_count += 1
        logging.info(f"Test cycle #{self.test_cycle_count} begins at time = {self.test_cycle_count * 15} seconds:")
        for endpoint in self.endpoints:
            status_code, latency = endpoint.check_health()
            domain = endpoint.url.split('/')[2]
            self.availability_percentages[domain]['total'] += 1

            if status_code and latency is not None:
                if 200 <= status_code < 300 and latency < 500:
                    self.availability_percentages[domain]['up'] += 1
                    result = "UP"
                else:
                    result = "DOWN"
            else:
                result = "DOWN"

            logging.info(
                f"Endpoint with name {endpoint.name} has HTTP response code {status_code} and "
                f"response latency {latency} ms => {result}"
            )

        logging.info(f"Test cycle #{self.test_cycle_count} ends.")
        for domain in self.domains:
            availability_percentage = self.calculate_availability_percentage(domain)
            logging.info(f"{domain} has {availability_percentage}% availability percentage")

    def run_health_checks(self):
        """
        Runs the health checks on the endpoints.
        """
        try:
            while True:
                self.log_availability_percentages()
                time.sleep(15)
        except KeyboardInterrupt:
            pass
