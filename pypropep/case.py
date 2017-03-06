from cpropep._cpropep import ffi, lib

class GenericCase(object):
    '''
    A generic container class for cpropep case's.
    The GenericCase is equivalent to the "TP" option in cpropep where 
    temperature and pressure are specified for the equillibrium calculation.
    '''
    def __init__(self, T=300., P=1.):
        super(Case, self).__init__()
        self._equil = ffi.new("equilibrium_t *")
        
        self._equil.