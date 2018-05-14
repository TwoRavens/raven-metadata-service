{% for one_var in var_list %}
.. data:: {{ one_var.name }}

    {% if one_var.description %}{{ one_var.description|safe }}{% endif %}

    {% if one_var.types %}* **types**: {{ one_var.types|join:" or "|safe }}{% endif %}
    {% if one_var.type %}* **type**: {{ one_var.type|safe }}{% endif %}
    {% if one_var.enum %}* **possible values**: {{ one_var.enum|join:", "|safe }}{% endif %}
    
{% endfor %}
