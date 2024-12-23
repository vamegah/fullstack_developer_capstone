import os
import requests
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv('backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url', default="http://localhost:5050/"
)


def get_request(endpoint, **kwargs):
    """
    Perform a GET request to the specified backend
    endpoint with optional query parameters.

    Args:
        endpoint (str): The API endpoint to call.
        **kwargs: Optional query parameters to include in the request.

    Returns:
        dict: The JSON response from the API, or None if an error occurs.
    """
    params = "&".join([f"{key}={value}" for key, value in kwargs.items()])
    request_url = f"{backend_url}{endpoint}?{params}"

    print(f"GET from {request_url}")
    try:
        response = requests.get(request_url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as err:
        print(f"Request error: {err}")
        return None


def post_review(data_dict):
    """
    Perform a POST request to insert a review into the backend.

    Args:
        data_dict (dict): The data to send in the POST request.

    Returns:
        dict: The JSON response from the API, or None if an error occurs.
    """
    request_url = f"{backend_url}/insert_review"
    try:
        response = requests.post(request_url, json=data_dict, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as err:
        print(f"Request error: {err}")
        return None


def analyze_review_sentiments(text):
    """
    Analyze the sentiment of the given text using the sentiment analyzer.

    Args:
        text (str): The text to analyze.

    Returns:
        dict: The JSON response from the sentiment analyzer,
        or None if an error occurs.
    """
    request_url = f"{sentiment_analyzer_url}analyze/{text}"

    try:
        response = requests.get(request_url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as err:
        print(f"Request error: {err}")
        return None
