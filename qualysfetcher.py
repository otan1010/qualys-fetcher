import logging
import re
import json

import requests
from requests.auth import HTTPBasicAuth
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from urllib.parse import urlparse,parse_qs
from bs4 import BeautifulSoup as bs

import xmltodict

from configuration import Configuration
from api import get_session

LOG = logging.getLogger(__name__)

def fetch(endpoint):
    conf = Configuration().get_endpoint(endpoint)
    session = get_session(endpoint)

    write_to = conf.get("options").get("write_to")
    url = conf.get("url")
    headers = conf.get("headers")
    params = conf.get("params")
    username = conf.get("credentials").get("username")
    password = conf.get("credentials").get("password")

    truncation = 1
    while truncation:
        truncation = 0
        response = session.get(url, headers=headers, params=params, auth=HTTPBasicAuth(username, password))
        print(response.headers.get("Content-Type"))
        text = response.text

        bs_content = bs(text, features="xml")

        try:
            new_url = bs_content.find("WARNING").find("URL").text
            new_url_p = urlparse(new_url)
            new_query = parse_qs(new_url_p.query)
            new_id = new_query.get("id_min")
            new_id = new_id[0]
            print(new_id)
        except Exception as err:
            new_id = None
            LOG.debug(err)

        if new_id:
            params['id_min'] = new_id
        else:
            truncation = 0

        try:
            items = bs_content.find("RESPONSE")
            items = items.find(re.compile("_LIST"))
            list_name = items.name
            items = items.find_all(recursive=False)
        except Exception as err:
            LOG.error(err)

        out = "data/" + write_to
        with open(out, 'a') as file:
            for item in items:
                item = xmltodict.parse(str(item))

                if list_name == "HOST_LIST":

                    host = item.get("HOST")

                    tracking_method = host.get('TRACKING_METHOD')
                    ip = host.get('IP')
                    host_id = host.get('ID')
                    asset_id = host.get('ASSET_ID')
                    qg_hostid = host.get('QG_HOSTID')

                    detections = host.get("DETECTION_LIST").get("DETECTION")
                    if isinstance(detections, list):
                        for detection in detections:

                            detection['ASSET_DATA'] = dict()
                            detection['ASSET_DATA']['TRACKING_METHOD'] = tracking_method
                            detection['ASSET_DATA']['HOST_ID'] = host_id
                            detection['ASSET_DATA']['ASSET_ID'] = asset_id
                            detection['ASSET_DATA']['IP'] = ip
                            detection['ASSET_DATA']['QG_HOSTID'] = qg_hostid
                            file.write(json.dumps(detection))
                            file.write("\n")

                    else:
                            detections['ASSET_DATA'] = dict()
                            detections['ASSET_DATA']['TRACKING_METHOD'] = tracking_method
                            detections['ASSET_DATA']['HOST_ID'] = host_id
                            detections['ASSET_DATA']['ASSET_ID'] = asset_id
                            detections['ASSET_DATA']['IP'] = ip
                            detections['ASSET_DATA']['QG_HOSTID'] = qg_hostid
                            file.write(json.dumps(detections))
                            file.write("\n")
                else:
                    try:
                        file.write(json.dumps(item))
                        file.write("\n")
                    except TypeError as err:
                        LOG.error(err)
