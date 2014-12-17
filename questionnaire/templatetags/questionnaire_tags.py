from django import template


register = template.Library()


@register.filter(name='addattr')
def addattr(field, attributes):
    attrs = {}
    definitions = attributes.split(',')

    for definition in definitions:
        name, value = definition.split(':')
        attrs[name] = value

    return field.as_widget(attrs=attrs)


def check_type(obj, stype):
    try:
        t = obj.__class__.__name__
        return t.lower() == str(stype).lower()
    except:
        pass
    return False
register.filter('obj_type', check_type)


@register.filter(name='field_type')
def field_type(field, ftype):
    return check_type(field.field.widget, ftype)


@register.filter(name='is_dm')
def is_data_manager(user):
    return user.groups.filter(name='Data Manager').exists()


@register.filter(name='is_pi')
def is_principal_investigator(user):
    return user.groups.filter(name='Principal Investigator').exists()


@register.filter(name='is_clerk')
def is_data_clerk(user):
    return user.groups.filter(name='Data Clerk').exists()