JSON Output Structure
============================

This document describes the structure of JSON string returned by our service.

Overview
--------

Our service will return a JSON string that contains four main blocks: Self Section, Dataset-level information,
Variable Section and Variable Display section. Below is an example of the output.

.. code-block:: json

   {
     "self":{
            ...metadata of the output...
     },
     "dataset": {
            ...metadata of the input dataset...
     },
     "variables":{
        "var_1":{
            ...statistic of var_1...
        },
        "var_2":{
            ...statistic of var_2...
        },
        ...
        "var_n":{
            ...statistic of var_n...
        },
      },
      "variableDisplay":{
        "var_1":{
            ...display setting of var_1...
        },
        "var_2":{
            ...display setting of var_2...
        },
        ...
        "var_n":{
            ...display setting of var_n...
        },
      },
    }



Self Section
----------------------------
.. note::

    - This section contains the information about the process task.


.. include:: self_section.rst


Dataset Section
----------------------------
.. note::

    - This section contains the important parameters of preprocess file at dataset level.


.. include:: dataset_section.rst


Variable Section
----------------------------


.. note::

    - Except **invalid** block, for all numeric calculations, missing values are ignored.
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


.. include:: custom_statistics_section.rst