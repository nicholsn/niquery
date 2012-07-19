__author__ = 'nolan'

import inspect

class Inspector(object):
    """
    Inspector is a tool for extracting information about a given class and its methods.

    Within the Pryo framework client proxies have no way of knowing about what services are available to them. There
    could be an xml file or other descriptor that describes the methods etc. but this is a potential solution that
    simply returns a dictionary where the keys are methods and the values are parameters.
    """

    def __init__(self, klass):
        self.services = {}
        for name, method in inspect.getmembers(klass, inspect.ismethod):
            if not name.startswith('_'):
                (args, varargs, varkw, defaults) = inspect.getargspec(method)
                self.services[name] = {'args':args,'varargs':varargs,'varkw':varkw,'defaults':defaults}

    def get_services(self):
        return self.services