
.. data:: variableName

    Name of the variable (column).

    * **type**: String

.. data:: description

    Brief explanation of the variable.

    * **type**: String

.. data:: numchar

    The type of this variable (column).

    * **type**: String
    * **possible values**: 'character', 'numeric'

.. data:: nature

    The type of this variable (from statistic perspective), below is the table of possible values.

    +-----------+------------------------------------------------------------+
    |    Name   |                   Definition                               |
    +-----------+------------------------------------------------------------+
    |  Nominal  | Just names, IDs                                            |
    +-----------+------------------------------------------------------------+
    |  Ordinal  | Have/Represent rank order                                  |
    +-----------+------------------------------------------------------------+
    |  Interval | Has a fixed size of interval between data points           |
    +-----------+------------------------------------------------------------+
    |  Ratio    | Has a true zero point (e.g. mass, length)                  |
    +-----------+------------------------------------------------------------+
    |  Percent  | Namely, [0.0, 1.0] or [0, 100]%                            |
    +-----------+------------------------------------------------------------+

    * **type**: String

.. data:: binary

    A boolean flag indicates whether this variable is a binary variable or not.


    * **type**: Boolean

.. data:: interval

    Indicate whether the variable is either continuous or discrete, if it's a numeric variable.

    * **type**: String
    * **possible values**: 'continuous', 'discrete' or 'NA'

.. data:: time

    Currently not available, it should return the format of timestamp if this variable is a timestamp.

    * **type**: String/None

.. data:: invalidCount

    Counts the number of invalid observations, including missing values, nulls, NA's and any observation with a value enumerated in invalidSpecialCodes.

    * **type**: Integer

.. data:: validCount

    Counts the number of valid observations

    * **type**: Integer

.. data:: uniqueCount

    Count of unique values, including invalid observations.

    * **type**: Integer

.. data:: median

    .. note::
        - This attribute may have incorrect value, fix is needed.

    A central value in the distribution such that there are as many values equal or above, as there are equal or below this value.
    It will be 'NA' if the data is not numerical.

    * **type**: Numeric/String

.. data:: mean

    Average of all numeric values, which are not contained in invalidSpecialCodes.
    It will be 'NA' if the data is not numerical.

    * **type**: Numeric/String

.. data:: max

    Largest numeric value observed in dataset, that is not contained in invalidSpecialCodes.
    It will be 'NA' if the data is not numerical.

    * **type**: Numeric/String

.. data:: min

    Least numeric value observed in dataset, that is not contained in invalidSpecialCodes.
    It will be 'NA' if the data is not numerical.

    * **type**: Numeric/String

.. data:: mode

    Value that occurs most frequently.  Multiple values in the case of ties.

    * **type**: List of String/Numeric

.. data:: modeFreq

    Number of times value of mode is observed in variable.

    * **type**: Integer

.. data:: fewestValues

    Value that occurs least frequently.  Multiple values in the case of ties.

    * **type**: List of String/Numeric

.. data:: fewestFreq

    Number of times value of fewestValues is observed in variable.

    * **type**: Integer

.. data:: midpoint

    The value equidistant from the reported min and max values.

    * **type**: Numeric/String

.. data:: midpointFreq

    Number of observations with value equal to midpoint.

    * **type**: Integer

.. data:: stdDev

    Standard deviation of the values, measuring the spread between values, specifically using population formula.

    * **type**: Numeric

.. data:: herfindahlIndex

    Measure of heterogeneity of a categorical variable which gives the probability that any two randomly sampled observations have the same value.

    * **type**: Numeric

.. warning::
    - Following attributes may be moved to **Variable Display Section** in the future.

.. data:: plotValues

    Contains the y-value of the plot, available while the **plot_type** is PLOT_BAR

    * **types**: List of Numeric

.. data:: pdfPlotType

    Describes default type of plot appropriate to represent the distribution of this variable.

    * **type**: String/Null
    * **possible values**: PLOT_BAR, PLOT_CONTINUOUS or None

.. data:: pdfPlotX

    A list of number that specifies the x-coordinate of corresponding points of the probability density function.

    * **types**: List of Numeric/Null

.. data:: pdfPlotY

    A list of number that specifies the y-coordinate of corresponding points of the probability density function.

    * **types**: List of Numeric/Null

.. data:: cdfPlotType

    Describes default type of plot appropriate to represent the cumulative distribution of variable.

    * **type**: String/Null
    * **possible values**: PLOT_BAR, PLOT_CONTINUOUS or None

.. data:: cdfPlotX

    A list of number that specifies the x-coordinate of corresponding points of the cumulative distribution function.

    * **types**: List of Numeric/Null

.. data:: cdfPlotY

    A list of number that specifies the x-coordinate of corresponding points of the cumulative distribution function.

    * **types**: List of Numeric/Null
