# Endpoint Health Checker

This project implements a program to check the health of a set of HTTP endpoints. It periodically sends requests to the specified endpoints and calculates the availability percentage for each domain.

## Installation

1. Clone the repository:

``` sh
git clone https://github.com/peng-shan/health-check-app.git
```

2. Install the required dependencies:

``` sh
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```


## Usage

1. Start the Flask application:

``` sh
python app.py
```

2. Open another terminal window and run the health checker:

``` sh
python health_check_app.py
```


3. When prompted, enter the path to the YAML configuration file (`endpoints.yaml`):

Enter the path to the YAML configuration file: endpoints.yaml


4. The health checker will start sending requests to the endpoints and calculate the availability percentages. The results will be logged to the console.

5. To stop the health checker, press `Ctrl+C`.

## Testing

To run the unit tests, use the following command:

``` sh
pytest
```


## Customization

- Modify the `endpoints.yaml` file to specify the endpoints you want to monitor.

- Adjust the code in `app.py` to customize the Flask application and add additional endpoints.

- Modify the code in `health_check_app.py` to change the health check intervals or add additional functionality.

## Docker Support

Alternatively, you can use Docker to run the application:

1. Build the Docker image:

``` sh
docker build -t endpoint-checker .
```

2. Run the Docker container:

``` sh
docker run -it --rm endpoint-checker
```

3. Follow the prompts to provide the path to the YAML configuration file.




