

.. data:: variableName

    Name of the variable


    * **type**: string



.. data:: description

    Brief explanation of the variable


    * **type**: string



.. data:: numchar

    Describes the variable as numeric or character valued


    * **type**: string
    * **possible values**: character, numeric


.. data:: nature

    Describes the classification of data into Nominal, Ordinal, Ratio, Interval, Percentage.


    * **type**: string
    * **possible values**: interval, nominal, ordinal, percent, ratio, other


.. data:: binary

    Signifies that the data can only take two values


    * **type**: boolean



.. data:: interval

    Describes numeric variables as either continuously valued, or discretely valued


    * **type**: string
    * **possible values**: continuous, discrete


.. data:: time

    Signifies that the variable describes points in time






.. data:: invalidCount

    Counts the number of invalid observations, including missing values, nulls, NA's and any observation with a value enumerated in invalidSpecialCodes


    * **type**: integer



.. data:: invalidSpecialCodes

    Any numbers that represent invalid observations


    * **type**: array



.. data:: validCount

    Counts the number of valid observations


    * **type**: integer



.. data:: uniqueCount

    Count of unique values, including invalid signifiers


    * **type**: integer



.. data:: median

    A central value in the distribution such that there are as many values equal or above, as there are equal or below this value.

    * **types**: number or string




.. data:: mean

    Average of all numeric values, which are not contained in invalidSpecialCodes

    * **types**: number or string




.. data:: max

    Largest numeric value observed in dataset, that is not contained in invalidSpecialCodes

    * **types**: number or string




.. data:: min

    Least numeric value observed in dataset, that is not contained in invalidSpecialCodes

    * **types**: number or string




.. data:: mode

    Value that occurs most frequently.  Multiple values in the case of ties.

    * **types**: array or string




.. data:: modeFreq

    Number of times value of mode is observed in variable

    * **types**: integer or string




.. data:: fewestValues

    Value that occurs least frequently.  Multiple values in the case of ties.

    * **types**: array or string




.. data:: fewestFreq

    Number of times value of fewestValues is observed in variable

    * **types**: integer or string




.. data:: midpoint

    The value equidistant from the reported min and max values

    * **types**: number or string




.. data:: midpointFreq

    Number of observations with value equal to minpoint

    * **types**: integer or string




.. data:: stdDev

    Standard deviation of the values, measuring the spread between values, specifically using population formula

    * **types**: number or string




.. data:: herfindahlIndex

    Measure of heterogeneity of a categorical variable which gives the probability that any two randomly sampled observations have the same value

    * **types**: number or string




.. data:: plotValues

    Plot points of a bar chart for tracing distribution of variable

    * **types**: object or string




.. data:: pdfPlotType

    Describes default type of plot appropriate to represent distribution of variable

    * **types**: string or null




.. data:: pdfPlotX

    Plot points along x dimension for tracing distribution of variable

    * **types**: array or null




.. data:: pdfPlotY

    Plot points along y dimension for tracing distribution of variable

    * **types**: array or null




.. data:: cdfPlotType

    Describes default type of plot appropriate to represent cumulative distribution of variable

    * **types**: string or null




.. data:: cdfPlotX

    Plot points along x dimension for tracing cumulative distribution of variable

    * **types**: array or null




.. data:: cdfPlotY

    Plot points along y dimension for tracing cumulative distribution of variable

    * **types**: array or null




.. data:: interpretation

    Object containing descriptors to interpret variable

    * **types**: object or string




.. data:: tworavens

    Object containing metadata specifically used by TwoRavens platform

    * **types**: object or string
