import logging
import re
import csv
import io
import json

import xmltodict

from urllib.parse import urlparse,parse_qs
from bs4 import BeautifulSoup as bs

LOG = logging.getLogger(__name__)

class Parser():

    def __init__(self, content, content_type, endpoint, item_tag):
        self.content = content
        self.content_type = content_type
        self.endpoint = endpoint
        self.item_tag = item_tag
        self.footer = self.xml_get_id()

    def get_new_id(self):
        if self.footer:
            url = self.footer.get("WARNING").get("URL")
            url_p = urlparse(url)
            query = parse_qs(url_p.query)

            id_min = query.get("id_min")
            id_max = query.get("id_max")

            if id_min and id_max:
                new_id = { "id_min": id_min[0], "id_max": id_max[0] }
            elif id_max:
                new_id = { "id_max": id_max[0] }
            elif id_min:
                new_id = { "id_min": id_min[0] }

        else:
            new_id = None

        return new_id

    def get_items(self):
        if 'csv' in self.content_type:
            for item in self.csv_streamparse():
                pass

        elif 'xml' in self.content_type:
            for item in self.xml_streamparse():
                if "detection" in self.endpoint:
                    for detection in self.parse_detection(item):
                        yield json.dumps(detection)
                else:
                    yield json.dumps(item)

    def xml_get_id(self):
        in_footer = 0

        for row in io.StringIO(self.content):
            if "<WARNING>" in row:
                in_footer = 1
                footer = ''

            if in_footer:
                footer += row

            if "</WARNING>" in row:
                in_footer = 0
                footer = xmltodict.parse(footer)
                return footer

    def xml_streamparse(self):
        start = "<" + self.item_tag + ">"
        end = "</" + self.item_tag + ">"
        in_item = 0
        in_footer = 0

        for row in io.StringIO(self.content):
            if start in row:
                in_item = 1
                item = ''

            if in_item:
                item += row

            if end in row:
                in_item = 0

                item = xmltodict.parse(item)
                item = item[self.item_tag]
                yield item

    def csv_streamparse(self):
        data = self.content.splitlines()
        body = ""
        footer = ""
        begin_response_body = 0
        begin_footer = 0

        for row in data:

            if row == "----BEGIN_RESPONSE_BODY_CSV":
                begin_response_body = 1
                continue

            elif row == "----END_RESPONSE_BOo.StringIO(body)DY_CSV":
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

        if footer:
            footer = next(csv.DictReader(io.StringIO(footer)))
            self.footer = { "WARNING": footer }
        else:
            self.footer = None

        self.items = csv.DictReader(io.StringIO(body))

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
