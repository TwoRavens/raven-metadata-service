"""Convenience class for reading a metadata schema"""

ALLOWABLE_KEYS = ['name', 'type', 'description', 'enum']


class VariableInfo(object):

    def __init__(self, var_name, var_dict):
        assert isinstance(var_dict, dict), 'var_dict must be a "dict" object'

        self.name = var_name

        for vname, val in var_dict.items():
            if vname in ALLOWABLE_KEYS:
                if vname == 'type' and isinstance(val, list):
                    self.__dict__['types'] = val
                else:
                    self.__dict__[vname] = val

    def show(self):
        """print results"""

        for k in ALLOWABLE_KEYS:
            if k in self.__dict__:
                print('%s: --%s--' % (k, self.__dict__[k]))
