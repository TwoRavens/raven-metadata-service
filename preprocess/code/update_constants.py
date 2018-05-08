"""Constants related to update metadata requests
Will be switched to a JSON schema check

Example update request:
 {
    "preprocess_id": 5,
    "variable_updates": {
       "cylinders" : {
         "viewable": true,
         "omit": ["mean", "median"],
         "value_updates": {
             "numchar":"discrete",
             "nature": "ordinal"
         }
       },
       "mpg": {
         "viewable": false,
         "omit": [],
         "value_updates": {

         }
       }
    }
}
"""

VARIABLE_UPDATES = 'variableUpdates'

VIEWABLE_KEY = 'viewable'
OMIT_KEY = 'omit'
VALUE_UPDATES_KEY = 'valueUpdates'
