from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
def ru_plural(value, variants):
    variants = variants.split(",")
    value = abs(int(value))

    if value % 10 == 1 and value % 100 != 11:
        variant = 0
    elif value % 10 >= 2 and value % 10 <= 4 and \
            (value % 100 < 10 or value % 100 >= 20):
        variant = 1
    else:
        variant = 2

    return variants[variant]

@register.filter(is_safe=False)
@stringfilter
def truncate_naturaltime(value):
    """
    Обрезка результата naturaltime от первой запятой до конца строки.
    """
    if ',' in value:
        return value.split(',', 1)[0].strip()+' назад'
    return value

register.filter('truncate_naturaltime', truncate_naturaltime)
