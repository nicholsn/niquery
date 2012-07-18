__author__ = 'nolan'
import Pyro4 as pyro
import nibabel as nib

class ImageService(object):
    def __init__(self):
        pass

    def get_methods(self):
        methods = {}
        for methodname in ImageService.__dict__.keys():
            if not methodname.startswith('__'):
                for varname in ImageService.__dict__[methodname].__code__.co_varnames:
                    methods[methodname] = varname
        return methods

    def load(self,image):
        self.image = nib.load(image)

    def get_affine(self):
        return self.image.get_affine()

    def get_header(self):
        hdr = self.image.get_header()
        keys = hdr.keys()
        hdr_dict = {}
        for key in keys:
            hdr_dict[key] = hdr[key]
        return hdr_dict

    def get_data(self):
        data = self.image.get_data()
        return data

    def get_slice(self, axis, slice):
        data = self.image.get_data()
        return data

def main():
    imageservice=ImageService()
    pyro.Daemon.serveSimple(
            {
            imageservice: "example.imageservice"
        },
        ns=False)

if __name__=="__main__":
    main()