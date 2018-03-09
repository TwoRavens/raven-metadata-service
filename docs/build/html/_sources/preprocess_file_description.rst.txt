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
  - For non-numeric values, summary statistics such as **median** and **mean** are set to `null`.
    For example:

  .. code-block:: json

   {
    "median":null
   }

.. data:: varnameSumStat

  Variable name as defined in the source file.
  If no columns are specified, defaults to `col_1`, `col_2`, etc.

  .. code-block:: json

   {
    "varnameSumStat":"cylinder_count"
   }

.. data:: labl

  Variable label.
  - Defaults to an empty string.

  .. code-block:: json

   {
     "label" : "Cylinder count for combustion engine"
   }

  Default label.

  .. code-block:: json

   {
     "label" : ""
   }

.. data:: median

  Median for a *numeric* variable, with a default precision of ??
  For non-numeric values, or if all values are missing, this value is set to `null`.


  .. code-block:: json

   {
     "median" : 50
   }

.. data:: mean

 Mean for a *numeric* variable, with a default precision of ??
 For non-numeric values, or if all values are missing, this value is set to `null`.

 .. code-block:: json

  {
    "mean" : 50
  }

.. data:: mode

 The values of up to 5 of the most frequently occurring variables, in descending order.

 .. code-block:: json

  {
    "mode" : ["bananas", "apple", "grapes", "strawberries", "oranges"]
  }

 Another example:

 .. code-block:: json

  {
    "mode" : [1997, 1995, 1996]
  }
