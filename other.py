import logging

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from static import get_configuration

conf = get_configuration()
LOG = logging.getLogger(__name__)

def get_from_api():

    retry_strategy = Retry(
                            total=2,
                            status_forcelist=[429, 500, 502, 503, 504],
                            method_whitelist=["HEAD", "GET", "OPTIONS"]
                          )

    adapter = HTTPAdapter(max_retries=retry_strategy)

    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)

    try:
        r = http.get('https://httpbin.org/delay/3', timeout=2)
    except requests.exceptions.ConnectionError as e:
        LOG.warning(e)

    #if r.ok:
    #    print("ok", r.status_code)
    #else:
    #    print(r.status_code)
