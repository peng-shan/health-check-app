import requests
import logging

class Endpoint:
    def __init__(self, name, url, method='GET', headers=None, body=None):
        """
        Represents an HTTP endpoint.

        Args:
            name (str): A free-text name to describe the HTTP endpoint.
            url (str): The URL of the HTTP endpoint.
            method (str, optional): The HTTP method of the endpoint. Defaults to 'GET'.
            headers (dict, optional): The HTTP headers to include in the request. Defaults to None.
            body (str, optional): The HTTP body to include in the request. Defaults to None.
        """
        self.name = name
        self.url = url
        self.method = method
        self.headers = headers or {}
        self.body = body

    def check_health(self):
        """
        Performs an HTTP request to check the health of the endpoint.

        Returns:
            tuple: A tuple containing the status code and response latency.
        """
        try:
            response = requests.request(
                self.method, self.url, headers=self.headers, json=self.body, timeout=5
            )
            response.raise_for_status()
            return response.status_code, response.elapsed.total_seconds() * 1000
        except (requests.RequestException, ValueError) as e:
            logging.error(f"Error checking endpoint {self.name}: {e}")
            return None, None
