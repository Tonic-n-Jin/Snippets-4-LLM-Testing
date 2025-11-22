import requests
import logging
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from typing import Generator, Dict, Any

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class ApiClient:
    """
    Handles robust, paginated data ingestion from a third-party REST API.
    Includes retries, backoff, and auth.
    """
    
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.session = self._create_session(api_key)
        logging.info(f"API Client initialized for {base_url}")

    def _create_session(self, api_key: str) -> requests.Session:
        """Creates a session with retries and default auth headers."""
        session = requests.Session()
        session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })
        
        # Configure retries
        retries = Retry(
            total=5,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods={"HEAD", "GET", "OPTIONS"}
        )
        
        adapter = HTTPAdapter(max_retries=retries)
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        
        return session

    def get_paginated_data(self, endpoint: str, params: Dict[str, Any] = None) -> Generator[Dict[str, Any], None, None]:
        """
        Fetches all data from a paginated endpoint.
        Assumes cursor-based pagination via 'next' URL in response.
        """
        url = f"{self.base_url}/{endpoint}"
        if params:
            url += f"?{pd.io.common.urlencode(params)}"
        
        while url:
            try:
                response = self.session.get(url)
                response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
                
                data = response.json()
                
                # Yield each item in the main data list
                for item in data.get("results", []):
                    yield item
                
                # Get the next page URL
                url = data.get("pagination", {}).get("next_url")
                
                if url:
                    logging.info(f"Fetching next page: {url}")
                else:
                    logging.info("All pages fetched.")
                
                # Respect rate limits if specified
                if int(response.headers.get('X-RateLimit-Remaining', 10)) < 2:
                    logging.warning("Rate limit low, sleeping for 60s.")
                    time.sleep(60)

            except requests.exceptions.HTTPError as e:
                logging.error(f"HTTP error fetching {url}: {e}")
                break
            except requests.exceptions.ConnectionError as e:
                logging.error(f"Connection error fetching {url}: {e}")
                break
            except Exception as e:
                logging.error(f"An unexpected error occurred: {e}")
                break
