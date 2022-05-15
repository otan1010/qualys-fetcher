import logging

import requests
from requests.auth import HTTPBasicAuth
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from configuration import Configuration

LOG = logging.getLogger(__name__)

def get_session(endpoint):
    conf = Configuration().get_endpoint(endpoint)

    params = conf.get("params")
    url = conf.get("url")
    headers = conf.get("headers")
    creds = conf.get("credentials")

    session = requests.Session()

    session.params = params
    session.url = url
    session.headers = headers
    session.auth = HTTPBasicAuth(creds.get("username"), creds.get("password"))

    retry_strategy = Retry(
        total=2,
        status_forcelist=[429, 500, 502, 503, 504],
        method_whitelist=["HEAD", "GET", "OPTIONS"]
        )

    adapter = HTTPAdapter(max_retries=retry_strategy)

    session.mount("https://", adapter)
    session.mount("http://", adapter)

    return session
