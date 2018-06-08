.. data:: id

    unique id assigned by system to the custom statistic. e.g id_000001


    * **type**: string

.. data:: name

    Name of the custom statistic.


    * **type**: string

.. data:: variables

    list of variables involved in the custom statistic.

    * **type**: string

.. data:: images

    list of images associated with the custom statistic.

    * **type**: string

.. data:: value

    value of the custom statistic. e.g mean : `12`

    * **type**: string or null

.. data:: description

    brief description of the custom statistics.

    * **type**: string or null

.. data:: replication

    the concept/formula behind the custom statistic generation. e.g `sum of obs/ size`.

    * **type**: string or null

.. data:: display

    owner of the custom statistic has an option to display the statistic or not.
    This can be done by changing a value of **viewable** to true or false.

    Default: true

    * **type**: boolean

