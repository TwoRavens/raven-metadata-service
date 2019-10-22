.. data:: description

    A brief description that contains the link to the service which generate this output.


    * **type**: String

.. data:: created

    A timestamp shows when the task is created. (YYYY-MM-DD HH:MM:SS)


    * **type**: String

.. data:: preprocessId

    An automatic generated ID for current task -- Currently is 'None'.


    * **type**: Numeric/None

.. data:: version

    A number describes the version of current task.


    * **type**: Numeric

.. data:: schema(Optional)

    Contains the description of the schema. You need to specify the value of 'SCHEMA_INFO_DICT' if this block is required. We don't provide this information by default.

    +-----------+------------------------------------------------------------+
    | Attribute |                   Description                              |
    +-----------+------------------------------------------------------------+
    |    Name   | Name of the followed schema                                |
    +-----------+------------------------------------------------------------+
    |  Version  | Version of corresponding schema it applied                 |
    +-----------+------------------------------------------------------------+
    | SchemaUrl | Source url of the schema                                   |
    +-----------+------------------------------------------------------------+
    | SchemaDoc | Link to the corresponding schema                           |
    +-----------+------------------------------------------------------------+

    * **type**: Dict
