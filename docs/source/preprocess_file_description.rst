Preprocess File Description
===========================

This document describes the variables contained in the preprocess output file.

Preprocess Parameters
---------------------

.. data:: variables

  Dictionary containing variable metadata

  .. code-block:: json

   {
     "dataset": {
            ...dataset-level information...
     },
     "variables":{
        "var_1":{
            ...variable-level data...
        },
        "var_2":{
            ..variable-level data...
        }
      },
      "variableDisplay":{
        "var_1":{
            ...variable-level display data...
        }
      },
    }
    

Data for each variable
----------------------------


.. note::

    - Except for **invalid**, for all numeric calculations, missing values are ignored.
    - For non-numeric values, summary statistics such as **median** and **mean** are set to `"NA"`.
    For example:

        .. code-block:: json

         {
          "median":"NA"
         }


.. include:: defn_variables.rst
