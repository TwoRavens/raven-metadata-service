.. data:: {{ var_name }}

    Description of the variable.
    Defaults to some thing or is calculated by ....

    .. code-block:: json

        {
          "{{ var_name }}": {% if sample_val %}{{ sample_val }}{% else %}"var_value"{% endif %}
        }
