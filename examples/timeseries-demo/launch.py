"""
Created on Jul 27, 2012

@author: detwiler
"""
import hmac

import Pyro4

from niquery.config import Config
from niquery.niq import NIQ

def main():
    """
    Demo of the NIQuery framework
    """
    # create an HMAC key for local use
    HMAC = hmac.new("this-is-a-demo-key").hexdigest()

    # import the default config
    config = Config()

    # set HMAC_KEY for security
    Pyro4.config.HMAC_KEY = HMAC

    # start the nameserver
    ns = Pyro4.naming.NameServerDaemon()

    # bind a daemon to the host server
    daemon = Pyro4.Daemon()

    # instantiate the NIQ service
    niq=NIQ(daemon)
    print "Ready."
    daemon.requestLoop()

if __name__ == '__main__':
    main()