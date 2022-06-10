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

    truncation = 1
    while truncation:
        #truncation = 0
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
                        f.write(json.dumps(item) + "\n")

                    if "<WARNING>" in row:
                        footer = ''
                        in_footer = 1

                    if in_footer:
                        footer += row

                    if "</WARNING>" in row:
                        in_footer = 0

            if footer:
                LOG.info(footer)
                footer = xmltodict.parse(footer)
                footer = footer["WARNING"]

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
