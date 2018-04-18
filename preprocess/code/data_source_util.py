import json
class DataSourceUtil(object):
    def __init__(self,**kwargs):
        """ set data source"""
        self.output = {}
        self.has_error = False
        self.error_message = None

        self.name = kwargs.get('name')
        self.type = kwargs.get('type')
        self.format = kwargs.get('format')

        self.data =  {
            "type": self.type,
            "format": self.format,
            "name": self.name
       }
        if self.data:
            self.output = self.data
        else:
            self.has_error = True
            self.error_message = "data for json not available"



     # print("data source",self.output)
