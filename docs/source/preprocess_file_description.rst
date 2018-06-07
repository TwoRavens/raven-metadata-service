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

Self Section
----------------------------
.. note::

    - This section contains the structure and description of the preprocessed file.


.. include:: self_section.rst


Dataset Section
----------------------------
.. note::

    - This section contains the important parameters of preprocess file at dataset level.


.. include:: dataset_section.rst


Variable Section
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


Variable Display Section
----------------------------
.. note::

    - This section contains the modified object/parameters in the particular version of preprocessed dataset.


.. include:: variable_display_section.rst

Custom Statistics Section
----------------------------
.. note::

    - This section contains the custom statistics added by the user on the dataset.


.. include:: variable_display_section.rst