import logging
import re

import xmltodict

from urllib.parse import urlparse,parse_qs
from bs4 import BeautifulSoup as bs

LOG = logging.getLogger(__name__)

class Parser():

    def __init__(self, content, content_type, endpoint):
        self.content_type = content_type
        self.endpoint = endpoint

        if 'csv' in self.content_type:
            return None
        elif 'xml' in self.content_type:
            bs_content = bs(content, features="xml")

            items = bs_content.find("RESPONSE")
            items = items.find(re.compile("_LIST"))

            items = items.findChildren(recursive=False)

            self.items = [ xmltodict.parse(str(item)) for item in items ]

            self.footer = bs_content.find("WARNING")

            if self.footer:
                self.footer = xmltodict.parse(str(self.footer))

    def get_new_id(self):
        if self.footer:
            url = self.footer.get("WARNING").get("URL")
            url_p = urlparse(url)
            query = parse_qs(url_p.query)
            new_id = query.get("id_min")
            new_id = new_id[0]
        else:
            new_id = None

        return new_id

    def get_content(self):
        for item in self.items:

            #Remove the root key (ASSET_GROUP: {}, ASSET, HOST, etc.)
            for key, value in item.items():
                item = value

            if self.endpoint == "detection":
                for detection in self.parse_detection(item):
                    yield detection
            else:
                yield item

    def parse_detection(self, host):
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
                
                yield detection

        else:
                detections['ASSET_DATA'] = dict()
                detections['ASSET_DATA']['TRACKING_METHOD'] = tracking_method
                detections['ASSET_DATA']['HOST_ID'] = host_id
                detections['ASSET_DATA']['ASSET_ID'] = asset_id
                detections['ASSET_DATA']['IP'] = ip
                detections['ASSET_DATA']['QG_HOSTID'] = qg_hostid

                yield detections
