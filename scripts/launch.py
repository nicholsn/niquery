'''
Created on Jul 27, 2012

@author: detwiler
'''
import Pyro4
from niquery.config import Config
from niquery.niq import NIQ

def main():
    """

    """
    # import the default configuration
    config = Config()
    # set HMAC_KEY for security
    Pyro4.config.HMAC_KEY = config.HMAC_KEY
    # bind a daemon to the host server
    daemon = Pyro4.Daemon(host=config.HOST,port=config.PORT)
    # locate the name server
    ns = Pyro4.locateNS(host=config.NS_HOST,port=config.NS_PORT)
    # instantiate the NIQ service
    niq=NIQ(daemon)
    # register the NIQ service to the name server
    uri=daemon.register(niq)
    ns.register("niq." + config.LOCATION, uri)

    print "Ready."
    daemon.requestLoop()

if __name__ == '__main__':
    main()
