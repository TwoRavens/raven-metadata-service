Preprocess File Description
===========================

This document describes the variables contained in the preprocess output file.

Preprocess Parameters
---------------------

.. data:: variables

  Dictionary containing variable metadata

  .. code-block:: json

   {
     "variables":{
        "var_1":{
            ...variable specific data...
        },
        "var_2":{
            ..variable specific data...
        }
      }
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
