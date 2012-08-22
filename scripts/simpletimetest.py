'''
Created on Jul 27, 2012

@author: detwiler
'''
from niquery.plugins import *
from niquery.datacontainer import DataContainer
#from niquery.base.plugin import WorkflowProvider
from niquery.config import Config
import Pyro4
import thread
import time

daemon = None
        
def launch_server_daemon():
    # set HMAC_KEY for security
    Pyro4.config.HMAC_KEY = b'BF7FFE77BFABDB26B35CABC5528EC'
    # bind a daemon to the host server
    global daemon
    daemon = Pyro4.Daemon()
    daemon.requestLoop()

def main():
    """

    """
    #config = Config()
    #map(__import__, config.WORKFLOW_PLUGIN_MODULES)
    dc = DataContainer('project', 'subject', 'acquisition', 'resource', '/Users/detwiler/eclipse/workspace/SIG/Python/NIQueryService/data/20120308_1998_s001_func_rest.nii.gz')
    #st = SimpleTime()
    
    thread.start_new_thread(launch_server_daemon,())
    
    #print dc.get_data()
    
    #uri = register_object(config)
    
    # wait for server to start
    while True:
        time.sleep(1)
        if(daemon!=None):
            break

    uri = daemon.register(dc)
    #print uri
    
    #dc2 = Pyro4.Proxy(uri)
    #print dc2.get_resource_info()
    #print dc2.get_data().shape[3]
    
    print "workflow providers = "+str([(p,p.get_display_text()) for p in dc.get_workflow_providers()])
    workflow_providers =  dc.get_workflow_providers()
    for workflow in workflow_providers:
        desc = workflow.get_description()
        kwargs = {'dc_uri':uri}
        if 'args' in desc:
            for arg in desc['args']:
                if not (arg['name'] in kwargs):
                    value = raw_input("Enter value of "+arg['name']+": ")
                    kwargs[arg['name']] = value


        print workflow().execute(**kwargs)#(dc_uri=uri,x=12,y=12,z=12)
#        if workflow == niquery.plugins.simpletime.SimpleTime:
#            st = workflow()
    
    #print st.get_voxel_time_series(uri, 12, 12, 12)
    

if __name__ == '__main__':
    main()