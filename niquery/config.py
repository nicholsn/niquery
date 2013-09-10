__author__ = 'nolan'

# this will be used as the main configuration for a service


#import glob, imp
#from os.path import join, basename, splitext
#from plugins.filemapper import XnatFileMapper

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
        self.NS_HOST = 'localhost'#'www.niquery.org'
        self.NS_PORT = 9090
        self.HMAC_KEY = 'BF7FFE77BFABDB26B35CABC5528EC'
        self.LOCATION = 'HOME'
        # url where XCEDE xml can be accessed
        self.METADATA_URL = "http://axon.biostr.washington.edu/niq/stanford/xcede-nims.xml"
        # meant to be xml description of services, uri, generated?
        self.SERVICES = "<niq>test niq</niq>"

        #self.PLUGINS = XnatFileMapper
        
        self.FILE_URI_BASE = 'http://cni.stanford.edu/bobd/xcede/'
        self.FILE_PATH_BASE = '/Users/nolan/PycharmProjects/SNI/NIQueryService/data/'

        self.WORKFLOW_PLUGIN_MODULES = ['niquery.plugins.simpletime','niquery.plugins.workflow']
        #self.PLUGIN_DIR = '/Users/detwiler/eclipse/workspace/SIG/Python/NIQueryRepository/niquery/niquery/plugins'
        #self.MODULES = self.importPluginModulesIn(self.PLUGIN_DIR)
        #print self.MODULES
        
#    def importPluginModulesIn(self,dir):
#        return dict( self._load(path) for path in glob.glob(join(dir,'[!_]*.py')) )
    
#    def _load(self,path):
#        name, ext = splitext(basename(path))
#        return name, imp.load_source(name, path)

# base class for "FileMapping" extended by sever specific
