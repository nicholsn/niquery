"""
base class providing support for clients
"""
__author__ = 'nolan'

import Pyro4
from ..config import Config

class Client(object):
    def __init__(self):
        self.config = Config()
        self.get_services()

    def get_services(self):
        """
        return a list of services available on the niquery network and update services attribute
        """
        ns_proxy = Pyro4.locateNS(host=self.config.NS_HOST, port=self.config.NS_PORT)
        self.services = ns_proxy.list(prefix='niq')
        return self.services


