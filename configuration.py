import yaml
import json

class Configuration():

    def __init__(self, endpoint=None):
        with open('configuration.yml', 'r') as file:
            self.configuration = yaml.safe_load(file)

        self.endpoint = endpoint

    def __repr__(self):
        return "Configuration()"

    def __str__(self):
        return str(self.configuration)

    def get_logging(self):
        return self.configuration.get("logging")

    def get_static(self):
        return self.configuration.get("endpoints").get(self.endpoint).get("params").get("static")

    def get_dynamic(self):
        print(json.dumps(self.configuration.get("endpoints").get(self.endpoint).get("params").get("dynamic"), sort_keys=True, indent=4))
        return self.configuration.get("endpoints").get(self.endpoint).get("params").get("dynamic")
