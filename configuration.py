from datetime import datetime, timedelta

import yaml

class Configuration():

    def __init__(self):
        with open('configuration.yml', 'r') as file:
            self.configuration = yaml.safe_load(file)

    def __repr__(self):
        return "Configuration(endpoint=None)"

    def __str__(self):
        return str(self.configuration)

    def get_logging(self):
        return self.configuration.get("logging")

    def get_endpoint(self, endpoint):
        dynamic = self.get_dynamic_params(endpoint)
        static = self.get_static_params(endpoint)
        api = self.get_api()

        return {**static, **dynamic, **api}

    def get_api(self):
        return self.configuration.get("api")

    def get_static_params(self, endpoint):
        return self.configuration.get("endpoints").get(endpoint).get("params").get("static")

    def get_dynamic_params(self, endpoint):
        params = self.configuration.get("endpoints").get(endpoint).get("params").get("dynamic")

        results = {}

        for param in params:

            now = datetime.utcnow()

            p_type = params.get(param).get("param_type")
            p_format = params.get(param).get("format")
            p_subtract = params.get(param).get("subtract")
            p_replace = params.get(param).get("replace")

            if p_type == "timestamp":

                if p_subtract:
                    now = now - timedelta(**p_subtract)

                if p_replace:
                    now = now.replace(**p_replace)

                if p_format:
                    now = now.strftime(p_format)

                results[param] = now

#            elif p_type == "list":
#                pass

        return results
