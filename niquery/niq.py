__author__ = 'detwiler'

# consolodate NIQ.py Session.py Data Container and Status.py
# currently thinking that NIQ is main service that imports "plugin" services at runtime and hands out sessions
# plugin services could include a queryservice, imageservice, and workflowservice
# another way could be to define a base service class that is extended...

import Pyro4
from session import Session

class NIQ(object):

    def __init__(self, config, daemon):
        """
        NIQ is the main service providing class that hands out sessions to clients and publicises the services available
        at a given location.

        NIQ is instantiated with an instance of the Config class, which contains all parameters needed to create a
        niquery service
        """

        self.url = config.HOST
        self.metadata_url = config.METADATA_URL
        self.services = config.SERVICES
        self.daemon = daemon

    def get_info(self):
        return "service called with info: URL = "+self.url+", xml description = "+self.services

    def get_metadata_url(self):
        return self.metadata_url

    def create_session(self):
        session = Session(self.daemon)
        session_uri = self.daemon.register(session)
        return session_uri

def main():
    """

    """
    from niquery.config import Config

    # import the default configuration
    config = Config()
    # set HMAC_KEY for security
    Pyro4.config.HMAC_KEY = 'BF7FFE77BFABDB26B35CABC5528EC' #config.HMAC_KEY
    # bind a daemon to the host server
    daemon = Pyro4.Daemon(host=config.HOST,port=config.PORT)
    # locate the name server
    ns = Pyro4.locateNS(host=config.NS_HOST,port=config.NS_PORT)
    # instantiate the NIQ service
    niq=NIQ(config, daemon)
    # register the NIQ service to the name server
    uri=daemon.register(niq)
    ns.register("niq." + config.LOCATION, uri)

    print "Ready."
    daemon.requestLoop()

if __name__=="__main__":
    main()