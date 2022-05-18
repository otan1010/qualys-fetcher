import logging
import re
import csv
import io

import xmltodict

from urllib.parse import urlparse,parse_qs
from bs4 import BeautifulSoup as bs

LOG = logging.getLogger(__name__)

class Parser():

    def __init__(self, content, content_type, endpoint):
        self.content_type = content_type
        self.endpoint = endpoint

        if 'csv' in self.content_type:
            rows = content.splitlines()
            body = ""
            footer = ""
            begin_response_body = 0
            begin_footer = 0

            for row in rows:

                if row == "----BEGIN_RESPONSE_BODY_CSV":
                    begin_response_body = 1
                    continue

                elif row == "----END_RESPONSE_BODY_CSV":
                    begin_response_body = 0
                    continue

                elif row == "----BEGIN_RESPONSE_FOOTER_CSV":
                    begin_footer = 1
                    continue

                elif row == "----END_RESPONSE_FOOTER_CSV":
                    begin_footer = 0
                    continue

                elif row == "WARNING":
                    continue

                if begin_response_body:
                    body += row + "\n"
                elif begin_footer:
                    footer += row + "\n"

            self.items = csv.DictReader(io.StringIO(body))

            #Seems truncation works differently with CSV output, and is also not documented anywhere (?)
            #Skipping for now.
            self.footer = None

            #footer = next(csv.DictReader(io.StringIO(footer)))
            #self.footer = { "WARNING": footer }

        elif 'xml' in self.content_type:
            bs_content = bs(content, features="xml")

            items = bs_content.find("RESPONSE")
            items = items.find(re.compile("_LIST"))

            items = items.findChildren(recursive=False)

            self.items = []
            for item in items:
                item = xmltodict.parse(str(item))
                for key, value in item.items():
                    self.items.append(value)

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

            if self.endpoint == "detection":
                for detection in self.parse_detection(item):
                    yield detection
            else:
                yield item

    def parse_detection(self, host):
        asset_data = dict(TRACKING_METHOD=host.get('TRACKING_METHOD'),
                IP = host.get('IP'),
                HOST_ID = host.get('ID'),
                ASSET_ID = host.get('ASSET_ID'),
                QG_HOSTID = host.get('QG_HOSTID'))

        detections = host.get("DETECTION_LIST").get("DETECTION")
        if isinstance(detections, list):
            for detection in detections:

                detection['ASSET_DATA'] = asset_data

                yield detection

        else:
                detections['ASSET_DATA'] = asset_data

                yield detections
