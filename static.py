import logging
import logging.handlers
import yaml
import json
import sys

from pythonjsonlogger import jsonlogger

LOG = logging.getLogger(__name__)

def set_logging():

    conf = get_configuration().get("logging")

    default_format = conf.get("default_format")
    level = conf.get("level")
    file_out = conf.get("file_out")
    unit = conf.get("unit")
    count = conf.get("count")
    interval = conf.get("interval")

    default_handler = logging.handlers.TimedRotatingFileHandler(file_out,
                                                                when=unit,
                                                                interval=interval,
                                                                backupCount=count)

    formatter = jsonlogger.JsonFormatter(default_format)
    default_handler.setFormatter(formatter)

    logging.basicConfig(level=level,
                        handlers=[default_handler])

def get_configuration():

    path = 'config.yml'

    try:
        with open(path, 'r') as file:
            configuration = yaml.safe_load(file)

    except FileNotFoundError:
        print(f"File {path} not found!")
        sys.exit()

    except PermissionError:
        print(f"Insufficient permission to read {path}!")
        sys.exit()

    except IsADirectoryError:
        print(f"{path} is a directory!")
        sys.exit()

    except yaml.scanner.ScannerError as e:
        print(f"Unable to parse {path}: {e}")
        sys.exit()

    else:
        LOG.debug(f"Loaded {path} successfully.")

    return configuration
