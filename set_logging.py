import logging
import logging.handlers

from pythonjsonlogger import jsonlogger

from configuration import Configuration

def set_logging():

#    conf = Configuration().get_logging()
    conf = Configuration().logging

    fields = conf.get("fields")
    level = conf.get("level").upper()
    file_out = conf.get("file_out")
    unit = conf.get("unit")
    count = conf.get("count")
    interval = conf.get("interval")

    default_handler = logging.handlers.TimedRotatingFileHandler(file_out,
                                                                when=unit,
                                                                interval=interval,
                                                                backupCount=count)

    formatter = jsonlogger.JsonFormatter(fields)

    default_handler.setFormatter(formatter)

    logging.basicConfig(level=level,
                        handlers=[default_handler])
