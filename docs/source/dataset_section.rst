.. data:: description

    A brief description of input dataset. (Currently is null)


    * **type**: String/NULL

.. data:: unit of analysis

    Unknown definition. (Currently is null)


    * **type**: String/NULL

.. data:: structure

    The structure of the input dataset.


    * **type**: String

.. data:: rowCount

    number of observations in the dataset.


    * **type**: Integer

.. data:: variableCount

    number of variables in the dataset.


    * **type**: Integer

.. data:: dataSource(Optional)

    Contains some extra information about the raw file. You need to specify the value of 'data_source_info' when a process runner is created, if this block is required. This information is not provided by default.

    +-----------+------------------------------------------------------------+
    | Attribute |                   Description                              |
    +-----------+------------------------------------------------------------+
    |    Name   | Name of input file                                         |
    +-----------+------------------------------------------------------------+
    |    Type   | File type (.csv, .xlxs etc)                                |
    +-----------+------------------------------------------------------------+
    |  Format   | Format of the input file                                   |
    +-----------+------------------------------------------------------------+
    | fileSize  | Size of the file in bytes                                  |
    +-----------+------------------------------------------------------------+

    * **type**: Dict

.. data:: citation(Optional)

    Unknown definition. default is null.

    * **type**: String

.. data:: error

    A message shows the error happened during dataset-level analysis. This entity may not exist if there is no error occured.

    * **type**: String