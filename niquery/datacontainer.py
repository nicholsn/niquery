"""
Created on May 21, 2012

@author: detwiler
"""

import ConfigParser
import nibabel as nib

class DataContainer(object):
    """
    classdocs
    """
    # other image methods to consider
    # get_nibabl_object
    # get_nibabel_header
    # other metadata methods to consider


    def get_data(self):
        #print self.uri
        file_path = self.uri.replace(self.file_uri_base,self.file_path_base)
        #print file_path
        img = nib.load(file_path)
        data = img.get_data()
        return data

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

    def __init__(self, project, subject, acquisition, resource, uri):
        """
        Constructor
        """

        self.project = project
        self.subject = subject
        self.acquisition = acquisition
        self.resource = resource
        self.uri = uri

        config = ConfigParser.RawConfigParser()
        config.read('bdt_setup.cfg')

        self.file_path_base = config.get('FileMapping', 'file_path_base')
        self.file_uri_base = config.get('FileMapping', 'file_uri_base')
        
    