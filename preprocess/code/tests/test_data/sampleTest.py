import json
colnames = ['cylinders','mpg'];
editable_vars = ['numchar','nature'];
preprocess_json = {
               "$schema":"http://(link to eventual schema)/jjonschema/1-0-0#",
               "self":{
                  "description":"TwoRavens metadata generated by ....",
                  "created":"..time stamp..",
                  "preprocess_id":45,
                  "data_url":"http://metadata.2ravens-url.org/preprocess/data/45",
                  "format":"jsonschema",
                  "preprocess_version":"1-0-0",
                  "schema_version":"1.0.0"
               },
               "variables": {
                  "cylinders": {
                    "varnameTypes": "cylinders",
                     "numchar":"continuous",
                      "nature": "nominal",
                     "mean":213,
                     "median":34

                  },
                  "mpg":{
                        "varnameTypes": "mpg",
                      "numchar": "continuous",
                       "nature": " ordinal",
                       "mean": 313,
                       "median": 54

                   }
               },
               "variable_display":{
                  "cylinders":{
                     "viewable":"true",
                     "omit":[
                     ],
                     "label":"",
                     "images":{
                        "url1":{
                           "type":"pdf",
                           "description":"This is the density of the mpg variable.",
                           "dateCreated":"timestamp",
                           "version":"imagecreate v0.1"
                        }
                     }
                  },
                   "mpg":
{
                     "viewable":"true",
                     "omit":[
                     ],
                     "label":"",
                     "images":{
                        "url1":{
                           "type":"pdf",
                           "description":"This is the density of the mpg variable.",
                           "dateCreated":"timestamp",
                           "version":"imagecreate v0.1"
                        }
                     }
                  }
               }
}
attributes = ['numchar','nature','mean', 'median']

update_json =  {
            "preprocess_id": 45,
            "variable_updates": {
               "cylinders" : {
                  "viewable": True,
                 "omit": ["mean", "median"],
                 "label": {
                     "numchar":"discrete",
                     "nature": "ordinal"
                 }
               },
               "mpg": {
                 "viewable": False,
                 "omit": [],
                 "label": {

                 }
               }
            }
        }

access_object = update_json['variable_updates']

original_json =preprocess_json
access_obj_original = original_json['variables']
access_obj_original_display = original_json['variable_display']
a = list(access_obj_original)
for varname in a:
     print(varname)

# print("original variavles", access_obj_original)
# print("original displayvar", access_obj_original_display)
def modify_original(varname, omit_obj, viewable_obj, label_obj):
    # print("*** INFO WE GET FROM PARAM")
    # print("varname", varname)
    # print("omit_obj", omit_obj)
    # print("viewable_obj", viewable_obj)
    # print("lable", label_obj)

    if not varname in access_obj_original:
        print('"%s" was not found in the "variable" section of the metadata file' % varname)
        return

    elif not varname in access_obj_original_display:
        print('"%s" was not found in the "variable_display" section of the metadata file' % varname)
        return

    else:
        variable_obj = access_obj_original[varname]
        display_variable_obj = access_obj_original_display[varname]
        # print(variable_obj)
        """
        variable_obj contains : "numchar":"continuous",
                    "nature": "nominal",
                   "mean":213,
                   "median":34
        """
        # code for omit
        if omit_obj:
            # start deleting omit objects
            for omit_var in omit_obj:
                del variable_obj[omit_var]
            display_variable_obj['omit'] = omit_obj

        # code for viewable
        if viewable_obj is False:
            # print("delete", var)
            del access_obj_original[varname]
            display_variable_obj['viewable'] = False

        # code for label
        if label_obj:
            for att_name in attributes:
                if att_name in label_obj and att_name in editable_vars:
                    variable_obj[att_name] = label_obj[att_name]

            display_variable_obj['label'] = label_obj


access_object = update_json['variable_updates']
for varname in colnames:
    print(' level 1 var name', varname);
    omit_object = access_object[varname]['omit']
    viewable_object = access_object[varname]['viewable']
    label_object = access_object[varname]['label']

    modify_original(varname, omit_object, viewable_object, label_object)





print("*********")
print(original_json)
print("*********")

"""
output should be =
{
    "$schema": "http://(link to eventual schema)/jjonschema/1-0-0#",
    "self": {
        "description": "TwoRavens metadata generated by ....",
        "created": "..time stamp..",
        "preprocess_id": 45,
        "data_url": "http://metadata.2ravens-url.org/preprocess/data/45",
        "format": "jsonschema",
        "preprocess_version": "1-0-0",
        "schema_version": "1.0.0"
    },
    "variables": {
        "cylinders": {
            "numchar": "discrete",
            "nature": "ordinal",
            "mean": 213,
            "median": 34
        },
        "mpg": {
            "numchar": "continuous",
            "nature": " ordinal",
            "mean": 313,
            "median": 54
        }
    },
    "variable_display": {
        "cylinders": {
            "viewable": "true",
            "omit": [
                "mean",
                "median"
            ],
            "label": {
                "numchar": "discrete",
                "nature": "ordinal"
            },
            "images": {
                "url1": {
                    "type": "pdf",
                    "description": "This is the density of the mpg variable.",
                    "dateCreated": "timestamp",
                    "version": "imagecreate v0.1"
                }
            }
        },
        "mpg": {
            "viewable": false,
            "omit": [],
            "label": "",
            "images": {
                "url1": {
                    "type": "pdf",
                    "description": "This is the density of the mpg variable.",
                    "dateCreated": "timestamp",
                    "version": "imagecreate v0.1"
                }
            }
        }
    }
}



"""