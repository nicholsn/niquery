"""
Created on May 21, 2012

@author: detwiler
"""

import nibabel as nib
from config import Config
from .base.plugin import WorkflowProvider

class DataContainer(object):
    """
    classdocs
    """
    # other image methods to consider
    # get_nibabl_object
    # get_nibabel_header
    # other metadata methods to consider 
    
    def __init__(self, daemon, project, subject, acquisition, resource, uri):
        """
        Constructor
        """
        self.daemon = daemon
        self.project = project
        self.subject = subject
        self.acquisition = acquisition
        self.resource = resource
        self.uri = uri
        
        self.workflow_provider_types = WorkflowProvider.plugins.keys() #@UndefinedVariable

        #for wf_plugin in WorkflowProvider.plugins: #@UndefinedVariable
        #    wf_class_name = wf_plugin.__name__
        #    self.workflow_provider_types.apend(wf_class_name)
            
        self.workflow_providers = {}
        
        #self.workflow_providers = WorkflowProvider.plugins #@UndefinedVariable

        config = Config()
        self.file_path_base = config.FILE_PATH_BASE
        self.file_uri_base = config.FILE_URI_BASE
        
        #print self.uri
        file_path = self.uri.replace(self.file_uri_base,self.file_path_base)
        #print file_path
        self.img = nib.load(file_path)

    def get_data(self):
        data = self.img.get_data()
        return data
    
    def get_img(self):
        return self.img
 
    def get_uri(self):
        return self.uri

    def get_resource_info(self):
        return self.resource

    def get_acquisition_info(self):
        return self.acquisition

    def get_subject_info(self):
        return self.subject

    def get_project_info(self):
        return self.project
    
    def get_workflow_provider_types(self):
        return self.workflow_providers_types
    
    def get_workflow_for_classname(self, classname): # this needs to pass back uris, not objects
        if classname in self.workflow_providers:
            return self.daemon.uriFor(self.workflow_providers[classname])   
        else:
            plugin_uri = None
            plugin_cls = WorkflowProvider.plugins[classname] #@UndefinedVariable
            if plugin_cls is not None:
                plugin = plugin_cls()
                self.workflow_providers[classname] = plugin
                plugin_uri = self.daemon.register(plugin)
            return plugin_uri            
                    
    def get_workflow_provider_descriptions(self):
        return [x.get_description() for x in WorkflowProvider.plugins.values()] #@UndefinedVariable
    
    def get_workflow_description(self, classname):
        if classname in WorkflowProvider.plugins: #@UndefinedVariable
            return WorkflowProvider.plugins[classname].get_description()
        else:
            return None
    