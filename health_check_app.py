from health_check.health_checker import HealthChecker


if __name__ == '__main__':
    # Prompt the user for the path to the YAML configuration file, otherwise use the default
    file_path = input("Enter the path to the YAML configuration file: ")
    if not file_path:
        file_path = 'endpoints.yaml'

    # Prompt the user for the time interval, otherwise use the default
    time_interval = input("Enter the time interval (in seconds): ")
    if not time_interval:
        time_interval = 15
    else:
        time_interval = int(time_interval)

    # Create an instance of HealthChecker
    health_checker = HealthChecker(file_path, time_interval)

    # Load the endpoints from the YAML configuration file
    health_checker.load_endpoints()

    # Run the health checks
    health_checker.run_health_checks()
