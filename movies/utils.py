# utils.py
import requests
from django.conf import settings
from requests.auth import HTTPBasicAuth
import time


def fetch_movies_with_retries(retries=5, delay=1, backoff=2):
    """
    Fetch a list of movies from the third-party API with retry logic.
    Retries up to `retries` times, doubling the delay with each attempt.
    """
    attempt = 0
    while attempt < retries:
        try:
            response = requests.get(
                settings.MOVIE_API_URL,
                auth=(settings.MOVIE_API_ID, settings.MOVIE_API_SECRET),
                timeout=5,
                verify=False,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            attempt += 1
            print(attempt)
            if attempt == retries:
                raise Exception("Failed to fetch movies after multiple retries") from e
            time.sleep(delay)
            delay *= backoff
