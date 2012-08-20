"""
Created on May 21, 2012

@author: detwiler
"""

import nibabel as nib
from .base.plugin import WorkflowProvider

class DataContainer(object):
    """
    classdocs
    """
    # other image methods to consider
    # get_nibabl_object
    # get_nibabel_header
    # other metadata methods to consider
    
    workflow_providers = WorkflowProvider.plugins #@UndefinedVariable
    
    def __init__(self, config, project, subject, acquisition, resource, uri):
        """
        Constructor
        """
        self.project = project
        self.subject = subject
        self.acquisition = acquisition
        self.resource = resource
        self.uri = uri

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
        
    def get_workflow_providers(self):
        return self.workflow_providers
    