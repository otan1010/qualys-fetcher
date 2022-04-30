import yaml
import json
from datetime import datetime, timedelta

class Configuration():

    def __init__(self, endpoint=None):
        with open('configuration.yml', 'r') as file:
            self.configuration = yaml.safe_load(file)

        self.endpoint = endpoint

    def __repr__(self):
        return "Configuration(endpoint=None)"

    def __str__(self):
        return str(self.configuration)

    def get_logging(self):
        return self.configuration.get("logging")

    def get_static_params(self):
        return self.configuration.get("endpoints").get(self.endpoint).get("params").get("static")

    def get_dynamic_params(self):
        params = self.configuration.get("endpoints").get(self.endpoint).get("params").get("dynamic")
        
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

                now = now.strftime(p_format)

                results[param] = now

            elif p_type == "list":
                pass

        return results
