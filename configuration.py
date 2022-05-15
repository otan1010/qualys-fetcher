from datetime import datetime, timedelta

import yaml

class Configuration():

    def __init__(self, file_path="configuration.yml", cred_path="credentials.yml"):
        self.cred_path = cred_path
        self.file_path = file_path

        with open(self.cred_path, "r") as file:
            self.credentials = yaml.safe_load(file)

        with open(self.file_path, "r") as file:
            self.all = yaml.safe_load(file)

        self.request = self.all.get("request")
        self.logging = self.all.get("logging")
        self.endpoints = self.all.get("endpoints")
        self.options = self.all.get("options")

    def __repr__(self):
        return f"Configuration(file_path={self.file_path}, credentials={self.cred_path})"

    def __str__(self):
        return str(self.all)

    def get_schedules(self):
        results = {}

        for key, value in self.endpoints.items():
            results[key] = value.get("schedule")

        return results

    def get_endpoint(self, endpoint):
        headers = self.get_headers()
        dynamic = self.get_dynamic_params(endpoint)
        static = self.get_static_params(endpoint)
        url = self.get_url(endpoint)
        options = self.get_options(endpoint)
        creds = self.credentials

        return { "params": { **static, **dynamic }, "url": url, "headers": headers, "credentials": creds, "options": options }

    def get_url(self, endpoint):
        domain = self.request.get("domain")
        path = self.request.get("path")
        endpoint = self.endpoints.get(endpoint).get("endpoint")

        url = domain + path + endpoint

        return url

    def get_headers(self):
        return self.request.get("headers")

    def get_options(self, endpoint):
        options = self.endpoints.get(endpoint).get("options")

        return options

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

        if params:
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

        #If format is not specified this will return datetime object,
        #else formatted date string
        return results
