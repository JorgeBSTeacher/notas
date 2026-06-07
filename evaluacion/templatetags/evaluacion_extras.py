from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    if dictionary is None:
        return None
    return dictionary.get(key)


@register.filter
def ud_key(unidad):
    """Return str(unidad.id) or '0' if unidad is None (safe for template)."""
    if unidad is None:
        return "0"
    return str(unidad.id)
