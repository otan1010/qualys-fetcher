import logging
import json
from os import replace
from urllib.parse import urlparse, parse_qs

import xmltodict

from requests.auth import HTTPBasicAuth

from configuration import Configuration
from get_session import get_session

import datetime

LOG = logging.getLogger(__name__)

def fetch(endpoint):
    conf = Configuration().get_endpoint(endpoint)
    session = get_session(endpoint)

    write_to = conf.get("options").get("write_to")
    item_tag = conf.get("options").get("item_tag")
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
        LOG.debug(err)

    item_count = 0
    yield_count = 0
    truncation = 1
    while truncation:
        truncation = 0

        now = datetime.datetime.now()
        print(now)
        LOG.info(params)

        with session.get(url, headers=headers, params=params, auth=HTTPBasicAuth(username, password), stream=True) as r:
            LOG.info(r)
            LOG.info(r.headers)

            with open(out, 'a') as f:

                start = "<" + item_tag + ">"
                end = "</" + item_tag + ">"
                in_item = 0
                in_footer = 0
                footer = None
                new_id = None

                for row in r.iter_lines():
                    row = row.decode("utf-8")

                    if start in row:
                        in_item = 1
                        item = ''

                    if in_item:
                        item += row

                    if end in row:
                        in_item = 0

                        item = xmltodict.parse(item)
                        item = item[item_tag]

                        item_count += 1
                        for i in get_endpoint_items(endpoint, item):
                            f.write(json.dumps(i) + "\n")
                            yield_count += 1

                    if "<WARNING>" in row:
                        footer = ''
                        in_footer = 1

                    if in_footer:
                        footer += row

                    if "</WARNING>" in row:
                        in_footer = 0

            if footer:
                footer = xmltodict.parse(footer)
                footer = footer["WARNING"]
                LOG.info(footer)

                url = footer.get("URL")
                url_p = urlparse(url)
                query = parse_qs(url_p.query)

                id_min = query.get("id_min")
                id_max = query.get("id_max")

                if id_min and id_max:
                    new_id = {"id_min": id_min[0], "id_max": id_max[0]}
                elif id_max:
                    new_id = {"id_max": id_max[0]}
                elif id_min:
                    new_id = {"id_min": id_min[0]}

            if new_id:
                params.update(new_id)
            else:
                truncation = 0

            now = datetime.datetime.now()
            print(now)

    print(item_count)
    print(yield_count)

def get_endpoint_items(endpoint, item):
    if "detection" in endpoint:                        
        asset_data = dict(TRACKING_METHOD=item.get('TRACKING_METHOD'),
                          IP=item.get('IP'),
                          HOST_ID=item.get('ID'),
                          ASSET_ID=item.get('ASSET_ID'),
                          QG_HOSTID=item.get('QG_HOSTID'))

        detections = item.get("DETECTION_LIST").get("DETECTION")

        if isinstance(detections, list):
            for det in detections:
                RES = det.get('RESULTS')
                if RES:
                    det['RESULTS'] = (RES[:10000] + ' ... [TRUNCATED]') if len(RES) > 10000 else RES

                det['ASSET_DATA'] = asset_data
                yield det
        else:
            RES = detections.get('RESULTS')
            if RES:
                detections['RESULTS'] = (RES[:10000] + ' ... [TRUNCATED]') if len(RES) > 10000 else RES

            detections['ASSET_DATA'] = asset_data
            yield detections

    elif "knowledgebase" in endpoint:
        DIAG = item.get('DIAGNOSIS')
        item['DIAGNOSIS'] = (DIAG[:10000] + ' ... [TRUNCATED]') if len(DIAG) > 10000 else DIAG
        yield item

    else:
        yield item
