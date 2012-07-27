__author__ = 'nolan'

# this will be used as the main configuration for a service

from .plugins.filemapper import XnatFileMapper

class Config(object):
    """
    Configuration options for NIQuery service.

    Example:

    >>> from niquery.config import Config
    >>> from niquery.niq import NIQ
    >>> config = Config()
    >>> NIQ(config)

    """

    def __init__(self,host='localhost',port=9999):
        self.HOST = host
        self.PORT = port
        self.NS_HOST = 'www.niquery.org'
        self.NS_PORT = 9090
        self.HMAC_KEY = 'BF7FFE77BFABDB26B35CABC5528EC'
        self.LOCATION = 'HOME'
        # url where XCEDE xml can be accessed
        self.METADATA_URL = "http://axon.biostr.washington.edu/niq/stanford/xcede-nims.xml"
        # meant to be xml description of services, uri, generated?
        self.SERVICES = "<niq>test niq</niq>"

        self.PLUGINS = XnatFileMapper

# base class for "FileMapping" extended by sever specific
#git test