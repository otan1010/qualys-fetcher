import logging

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from configuration import Configuration

LOG = logging.getLogger(__name__)

class QualysFetcher():

    #def __init__(self, endpoint):
    def __init__(self):
        pass
    #    self.endpoint = endpoint

    def get_session_obj(self):
        retry_strategy = Retry(
            total=2,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "OPTIONS"]
            )

        adapter = HTTPAdapter(max_retries=retry_strategy)

        session = requests.Session()
        session.mount("https://", adapter)
        session.mount("http://", adapter)

        return session

    #def get(self, endpoint):
    def get(self):

        #conf = Configuration().get_endpoint(endpoint)
        session = self.get_session_obj()

        try:
            request = session.get('https://httpbin.org/delay/3', timeout=4)
            #request = session.get('https://httpbin.org/delay/3', timeout=2)
            return request
        except requests.exceptions.ConnectionError as err:
            LOG.warning(err)

        #if r.ok:
        #    print("ok", r.status_code)
        #else:
        #    print(r.status_code)
