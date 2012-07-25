"""
Classes that implement a mapping between data URIs and files on disk

This mapping is required for loading a file via Nibabel
"""
__author__ = 'nolan'

from ..base.plugin import FileMapperProvider

class XnatFileMapper(FileMapperProvider):
    def __init__(self):
        pass

    # given a query response, construct the absolute path to a nifti file on an xnat server
    # return a string to the file on disk
    # DataContainer will call XnatFileMapper during construction in order to load nifti via nibabels
