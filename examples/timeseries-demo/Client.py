'''
Created on May 2, 2012

@author: detwiler
'''

import Pyro4

class Client(object):
    '''
    classdocs
    '''

    def get_niq_services(self):
        niq_services = self.ns.list('niq')
        return niq_services
    
    def create_niq_for_service_name(self,service_name):
        niq_uri = self.ns.lookup(service_name)
        if self.ns == None :
            return None
        niq = Pyro4.Proxy(niq_uri)
        return niq
    
    def create_session_for_niq(self,niq):
        session_uri = niq.create_session()
        session=Pyro4.Proxy(session_uri)
        return session
    
    def create_session_for_service(self, service_name):
        services = self.get_niq_services()
        service = services[service_name]
        niq = Pyro4.Proxy(service)
        session_uri = niq.create_session()
        session=Pyro4.Proxy(session_uri)
        return session
    
    #def get_visualization_url(self,uri):
    #    return vis_mappings[uri]

    def __init__(self):
        '''
        Constructor
        '''
        ns_host = 'localhost'#'www.niquery.org'
        ns_port = 9090                                 
        self.ns=Pyro4.locateNS(host=ns_host,port=ns_port)
        
        #config.get('http://cni.stanford.edu/bobd/xcede/20120308_1998_s001_func_rest.nii.gz', 'http://cni.stanford.edu/bobd/xcede/20120308_1998_s001_func_rest.html')
        


#Pyro4.config.HMAC_KEY=b'BF7FFE77BFABDB26B35CABC5528EC'
#client = Client()
#session = client.create_session_for_service("niq.stanford")
#qid = 286
#args = {"http://cni.stanford.edu/bobd/xcede/xcede-nims.xml,male,25"}
#results = session.execute_param_query(qid,args)
#print results