from django import template

register = template.Library()


@register.filter(name='active_tab')
def active_tab(tab_to_open, tab):
    if str(tab_to_open) == str(tab):
        return 'active'
    else:
        return ''
