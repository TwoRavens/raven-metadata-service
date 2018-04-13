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
    If no column names are specified, defaults to `col_1`, `col_2`, etc.

    .. code-block:: json

        {
          "varnameSumStat": "cylinder count"
        }

.. data:: labl

    Variable label.  Defaults to an empty string.

    .. code-block:: json

       {
         "label" : "Cylinder count for combustion engine"
       }

    Default label.

    .. code-block:: json

     {
       "label" : ""
     }


.. data:: numchar

    Numchar attribute descirbes the classification of the data into two types `Character` and `Numeric`. Defaults
    Defaults to some thing or is calculated by ....

    .. code-block:: json

        {
          "numchar": "var_value"
        }

.. data:: nature

    Nature attribute describes the classification of data into `Nominal`,  `Ordinal`,  `Ratio`,  `Interval`,  `Percentage`. Defaults
    Defaults to some thing or is calculated by ....

    .. code-block:: json

        {
          "nature": "var_value"
        }

.. data:: binary

    Binary represents the data of variables in a form where they can only take two values `0` and `1`. Defaults
    Defaults to some thing or is calculated by ....

    .. code-block:: json

        {
          "binary": "var_value"
        }

.. data:: interval

    It referes to the representation of the variables in certain intervals of values. Defaults
    Defaults to some thing or is calculated by ....

    .. code-block:: json

        {
          "interval": "var_value"
        }

.. data:: time

    TODO: Description of the variable. Defaults
    Defaults to some thing or is calculated by ....

    .. code-block:: json

        {
          "time": "var_value"
        }

.. data:: invalid

    Invalid represents the count of missing values ( `NA`,`Null`, empty cells, etc) in the data of the given variable. Defaults
    Defaults to some thing or is calculated by ....

    .. code-block:: json

        {
          "invalid": 1234
        }

.. data:: valid

    It refers to the data in the variable anything but not `invalid`. Defaults
    Defaults to some thing or is calculated by ....

    .. code-block:: json

        {
          "valid": 1234
        }

.. data:: uniques

    Uniques represents the count of unique values in the data of the given variable. Defaults
    Defaults to some thing or is calculated by ....

    .. code-block:: json

        {
          "uniques": 1234
        }

.. data:: median

    Median for a *numeric* variable. It represents the value lying at the midpoint of a frequency distribution.
     For non-numeric values, or if all values are missing, this value is set to null..

    .. code-block:: json

        {
          "median": 1234
        }

.. data:: mean

    Mean for a *numeric* variable.It represents the average of the numbers in the data of the given variable.
    For non-numeric values, or if all values are missing, this value is set to null.


    .. code-block:: json

        {
          "mean": 1234.56
        }

.. data:: max

    It is the maximum value among the values of the variable. Defaults
    Defaults to some thing or is calculated by ....

    .. code-block:: json

        {
          "max": 1234
        }

.. data:: min

    Min represents the minimum or least value in the data of the given variable.
     Defaults Defaults to some thing or is calculated by ….

    .. code-block:: json

        {
          "min": 1234
        }

.. data:: mode

    The value of the most frequently occurring variable.  If more than
    multiple variable share the highest number of occurrences, up to the first 5 are displayed.
    In the example below, each of the 5 values occurred 20 times.

    .. code-block:: json

        {
          "mode" : ["bananas", "apple", "grapes", "strawberries", "oranges"]
        }

    Another example:

    .. code-block:: json

        {
          "mode" : [1999, 1998, 1997]
        }

.. data:: freqmode

    It is a part of mode which represents the `count/frequence` of the mode of the given variable. Defaults
    Defaults to some thing or is calculated by ....

    .. code-block:: json

        {
          "freqmode": 1234
        }

.. data:: fewest

    fewest represents the value of the least frequently occurring variable. If more than multiple variable share the highest number of occurrences, up to the first 5 are displayed. Defaults
    Defaults to some thing or is calculated by ....

    .. code-block:: json

        {
          "fewest": "var_value"
        }

.. data:: freqfewest

    It is a part of fewest which represents the `count/frequence` of the fewest of the given variable. Defaults
    Defaults to some thing or is calculated by ....

    .. code-block:: json

        {
          "freqfewest": 1234
        }

.. data:: mid

    TODO: Description of the variable. Defaults
    Defaults to some thing or is calculated by ....

    .. code-block:: json

        {
          "mid": "var_value"
        }

.. data:: freqmid

    It is a part of mid which represents the `count/frequence` of the mid of the given variable. Defaults
    Defaults to some thing or is calculated by ....

    .. code-block:: json

        {
          "freqmid": 1234
        }

.. data:: sd

    sd represents the `Standard deviation`, which is the measure of how spread out the numbers are in the data. Defaults
    Defaults to some thing or is calculated by ....

    .. code-block:: json

        {
          "sd": 1234
        }

.. data:: herfindahl

    TODO: Description of the variable. Defaults
    Defaults to some thing or is calculated by ....

    .. code-block:: json

        {
          "herfindahl": 1234
        }

.. data:: plotvalues

    It represents the array of the values to draw the `bar` plot. Defaults
    Defaults to some thing or is calculated by ....

    .. code-block:: json

        {
          "plotvalues": 1234
        }

.. data:: plottype
PlotType describes the type of plot on the basis of the data of the variable. It is mainly classified as `Bar` and `Continuous`. Defaults
    Defaults to some thing or is calculated by ....

    .. code-block:: json

        {
          "plottype": "var_value"
        }

.. data:: plotx

    plotx describes the x-coordinates of the plot drawn using the data of the given variable. Defaults
    Defaults to some thing or is calculated by ....

    .. code-block:: json

        {
          "plotx": 1234
        }

.. data:: ploty

    ploty describes the y-coordinates of the plot drawn using the data of the given variable. Defaults
    Defaults to some thing or is calculated by ....

    .. code-block:: json

        {
          "ploty": 1234
        }

.. data:: cdfplottype

    CDF : cumulative distribution function. The cdf plot represent the cumulative distribution of the data of the variable. Defaults
    Defaults to some thing or is calculated by ....

    .. code-block:: json

        {
          "cdfplottype": "var_value"
        }

.. data:: cdfplotx

    cdfplotx describes the x-coordinates of the `cdf plot` drawn using the data of the given variable. Defaults
    Defaults to some thing or is calculated by ....

    .. code-block:: json

        {
          "cdfplotx": 1234
        }

.. data:: cdfploty

    cdfploty describes the x-coordinates of the `cdf plot` drawn using the data of the given variable. Defaults
    Defaults to some thing or is calculated by ....

    .. code-block:: json

        {
          "cdfploty": 1234
        }

.. data:: defaultInterval

    It represents the user input for the interval from the interface if user wants the variable to have default interval.
    The definition of this remains the same as interval. Defaults
    Defaults to some thing or is calculated by ....

    .. code-block:: json

        {
          "defaultInterval": "var_value"
        }

.. data:: defaultNumchar

    It represents the user input for the numchar from the interface if user wants the variable to have default numchar. The definition of this remains the same as numchar
    Defaults to some thing or is calculated by ....

    .. code-block:: json

        {
          "defaultNumchar": "var_value"
        }

.. data:: defaultNature

    It represents the user input for the nature from the interface if user wants the variable to have default nature. The definition of this remains the same as nature
    Defaults to some thing or is calculated by ....

    .. code-block:: json

        {
          "defaultNature": "var_value"
        }

.. data:: defaultBinary

    It represents the user input for the binary from the interface if user wants the variable to have default binary. The definition of this remains the same as binary
    Defaults to some thing or is calculated by ....

    .. code-block:: json

        {
          "defaultBinary": "var_value"
        }

.. data:: defaultTime

    It represents the user input for the time from the interface if user wants the variable to have default time. The definition of this remains the same as time
    Defaults to some thing or is calculated by ....

    .. code-block:: json

        {
          "defaultTime": "var_value"
        }
