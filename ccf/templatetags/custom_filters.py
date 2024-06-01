from django import template

register = template.Library()


@register.filter(name='active_tab')
def active_tab(tab_to_open, tab):
    if str(tab_to_open) == str(tab):
        return 'active'
    else:
        return ''


# could instead have used builtin filter 'truncatechars'
@register.filter(name='truncate_field')
def truncate_field(content, limit):
    limit = int(limit)
    if len(content) <= limit:
        return content
    else:
        return content[:limit]+'...'
