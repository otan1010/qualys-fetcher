from datetime import datetime, timedelta

import yaml

class Configuration():

    def __init__(self, file_path="configuration.yml"):
        with open(file_path, "r") as file:
            self.all = yaml.safe_load(file)

        self.url = self.all.get("url")
        self.logging = self.all.get("logging")
        self.endpoints = self.all.get("endpoints")

    def __repr__(self):
        return "Configuration()"

    def __str__(self):
        return str(self.all)

    def get_endpoint(self, endpoint):
        dynamic = self.get_dynamic_params(endpoint)
        static = self.get_static_params(endpoint)
        url = self.get_url()

        return { "params": { **static, **dynamic }, "url": url }

    def get_url(self):
        domain = self.url.get("domain")
        path = self.url.get("path")

        url = domain + path

        return url

    def get_static_params(self, endpoint):
        params = self.endpoints.get(endpoint).get("params").get("static")

        return params

    def get_dynamic_params(self, endpoint):
        ts = self.parse_dynamic_ts(endpoint)

        return { **ts }

    def parse_dynamic_ts(self, endpoint):
        params = self.endpoints.get(endpoint).get("params").get("dynamic")

        results = {}
        now = datetime.utcnow()

        for param in params:

            p_now = now
            p_type = params.get(param).get("param_type")
            p_format = params.get(param).get("format")
            p_subtract = params.get(param).get("subtract")
            p_replace = params.get(param).get("replace")

            if p_type == "timestamp":

                if p_subtract:
                    p_now = p_now - timedelta(**p_subtract)

                if p_replace:
                    p_now = p_now.replace(**p_replace)

                if p_format:
                    p_now = p_now.strftime(p_format)

                results[param] = p_now

        return results
