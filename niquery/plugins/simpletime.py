'''
Created on Jul 13, 2012

@author: detwiler
'''
from ..base.plugin import WorkflowProvider
import numpy as np
import Pyro4
from ..config import Config

class SimpleTime(WorkflowProvider):
    '''
    classdocs
    '''
    
    display_text = "Input: x,y,z coordinate :: Output: array of values at x,y,z for each t in image"
    #description = "<workflow><comment>Input: x,y,z coordinate :: Output: array of values at x,y,z for each t in image</comment></workflow>"
    description = {
                   'comment':'Input: x,y,z coordinate :: Output: array of values at x,y,z for each t in image',
                   'args':[{'name':'dc_uri','data_type':str},{'name':'x','data_type':int},{'name':'y','data_type':int},{'name':'z','data_type':int}]
                   }
    
    def execute(self,**kwargs):
        return self.get_voxel_time_series(**kwargs)
    
    def get_voxel_time_series(self, dc_uri, x, y, z):
        config = Config()

        Pyro4.config.HMAC_KEY = config.HMAC_KEY#b'BF7FFE77BFABDB26B35CABC5528EC' #config.HMAC_KEY
        dc = Pyro4.Proxy(dc_uri)
        
        img = dc.get_img()     
        data = img.get_data()
        
        # TODO, should check dimensionality of input image
        time_dim = data.shape[3]
        result_array = np.zeros(time_dim)

        for tindex in range(time_dim):
            result_array[tindex] = data[x,y,z,tindex]
        return result_array


    def __init__(self):
        '''
        Constructor
        '''
        