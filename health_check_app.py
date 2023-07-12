import time
import yaml
import logging
from health_check.health_checker import HealthChecker

if __name__ == '__main__':
    file_path = input("Enter the path to the YAML configuration file: ")

    # Create an instance of HealthChecker
    health_checker = HealthChecker(file_path)

    # Load the endpoints from the YAML configuration file
    health_checker.load_endpoints()

    # Run the health checks
    health_checker.run_health_checks()
