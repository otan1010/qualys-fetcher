import logging
import re
import json
from os import replace

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

    out = "data/" + write_to
    prev = out + ".prev"

    try:
        replace(out, prev)
    except Exception as err:
        print(err)
        LOG.error(err)

    truncation = 1
    while truncation:
        response = session.get(url, headers=headers, params=params, auth=HTTPBasicAuth(username, password))

        content_type = response.headers.get("Content-Type")
        text = response.text

        parsed = Parser(text, content_type)
        new_id = parsed.get_new_id()
        list_name = parsed.get_list_name()

        if new_id:
            params['id_min'] = new_id
        else:
            truncation = 0

        with open(out, 'a') as file:
            for item in parsed.get_content():
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


class Parser():

    def __init__(self, content, content_type):
        #self.content = content
        self.content_type = content_type

        if 'csv' in self.content_type:
            return None
        elif 'xml' in self.content_type:
            bs_content = bs(content, features="xml")

            items = bs_content.find("RESPONSE")
            items = items.find(re.compile("_LIST"))
            self.list_name = items.name
            self.items = items.findChildren(recursive=False)

            self.footer = bs_content.find("WARNING")

    def get_list_name(self):
        #if 'csv' in self.content_type:
        #    return None
        #elif 'xml' in self.content_type:
        #    bs_content = bs(self.content, features="xml")

        #    items = bs_content.find("RESPONSE")
        #    items = items.find(re.compile("_LIST"))
        #    list_name = self.items.name

        return self.list_name

    def get_new_id(self):
        if 'csv' in self.content_type:
            return None
        elif 'xml' in self.content_type:
            bs_content = bs(self.content, features="xml")

            try:
                new_url = self.footer.find("URL").text
                new_url_p = urlparse(new_url)
                new_query = parse_qs(new_url_p.query)
                new_id = new_query.get("id_min")
                new_id = new_id[0]
            except Exception as err:
                new_id = None
                LOG.debug(err)

        return new_id

    def get_content(self):
        #if 'csv' in self.content_type:
        #    print(self.content)
        #elif 'xml' in self.content_type:
        #    bs_content = bs(self.content, features="xml")

#        try:
            #items = bs_content.find("RESPONSE")
            #items = items.find(re.compile("_LIST"))
            #items = items.findChildren(recursive=False)
            for item in self.items:
                item = xmltodict.parse(str(item))

                yield item
#        except Exception as err:
#            LOG.error(err)
