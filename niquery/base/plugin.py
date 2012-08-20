__author__ = 'nolan'

class PluginMount(type):
    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, 'plugins'):
            # This branch only executes when processing the mount point itself.
            # So, since this is a new plugin type, not an implementation, this
            # class shouldn't be registered as a plugin. Instead, it sets up a
            # list where plugins can be registered later.
            cls.plugins = []
        else:
            # This must be a plugin implementation, which should be registered.
            # Simply appending it to the list is all that's needed to keep
            # track of it later.
            cls.plugins.append(cls)


class WorkflowProvider:
    """
    Mount point for plugins which refer to workflow that can be performed.

    Plugins implementing this reference should provide the following attributes:

    =============  ========================================================
    display_text    provides a human readable description of workflow
    
    description     provides a formal (machine-pocessable) description
    =============  ========================================================
    """
    __metaclass__ = PluginMount
    
    def execute(self,**kwargs):
        raise NotImplementedError( "WorkflowProviders must implement this method" )
    
    def get_display_text(self):
        if hasattr(self,'display_text'):
            return self.display_text
        else:
            return 'no display text provided'
        
    def get_description(self):
        if hasattr(self,'description'):
            return self.description
        else:
            return 'no description provided'
        

class FileMapperProvider:
    """
    Mount point for plugins which refer to files on disk at a given database.

    Plugins implementing this reference should provide the following attributes:

    ========  ========================================================
    title     The text to be displayed, describing the action

    url       The URL to the view where the action will be carried out

    selected  Boolean indicating whether the action is the one
              currently being performed
    ========  ========================================================
    """
    __metaclass__ = PluginMount