__author__ = 'nolan'
import Pyro4
import nibabel as nib
import numpy as np
from utils import Inspector

class ImageService(object):
    def __init__(self):
        pass

    def get_services(self):
        """
        return a dictionary of methods for ImageService where the values are a dictionary of parameters
        used for introspection and potentially generating client code

        Example:

        >>> imageservice = Pyro4.Proxy(uri)
        >>> services = imageservice.get_services()
        >>> services['load']
        {'args': ['self', 'image'], 'defaults': None, 'varargs': None, 'varkw': None}

        """
        services = Inspector(ImageService)
        return services.get_services()

    def load(self,image):
        """
        load any image nibabel can read on the servers local file system
        """
        self.image = nib.load(image)

    def unload(self):
        """
        release a loaded image from memory
        """
        del self.image

    def get_affine(self):
        """
        returns the affine array from a given header
        """
        return self.image.get_affine()

    def get_header(self):
        """
        returns a dictionary of header keys and corresponding values

        Example:

        >>> imageservice = Pyro4.Proxy(uri)
        >>> header = imageservice.get_header()
        {'vox_offset': array(352.0, dtype=float32),'xyzt_units': array(10, dtype=uint8), ...}
        """
        hdr = self.image.get_header()
        keys = hdr.keys()
        hdr_dict = {}
        for key in keys:
            hdr_dict[key] = hdr[key]
        return hdr_dict

    def get_data(self):
        """
        returns a numpy array of a loaded image
        """
        data = self.image.get_data()
        return np.array(data)

    def get_slice(self,axis, slice):
        global slab
        data = np.array(self.image.get_data())
        slab = np.empty(data.shape,data.dtype)
        print axis
        if axis is axis:
            slab = np.squeeze(data[slice,:,:])
            print True
        elif axis is 'coronal':
            slab = np.squeeze(data[:,slice,:])
        elif axis is 'axial':
            slab = np.squeeze(data[:,:,slice])
        return slab

def main():
    imageservice=ImageService()
    Pyro4.Daemon.serveSimple(
            {
            imageservice: "example.imageservice"
        },
        ns=False)

if __name__=="__main__":
    main()