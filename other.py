import logging

from static import get_configuration

conf = get_configuration()
LOG = logging.getLogger(__name__)

def method1():
    LOG.info("TESTINGGGGGGGGGGGGG")
    print(conf)
