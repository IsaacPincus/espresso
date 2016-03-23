from __future__ import print_function
from espressomd.highlander import highlander
from espressomd import _system


@highlander
class System(_system.System):

    def __init__(self):
       _system.System.__init__(self)

    def __setattr__(self, name, value):
        try: self.__getattribute__(name)
        except AttributeError:
            raise AttributeError("System does not have the attribute", name)
        super(System, self).__setattr__(name, value)
