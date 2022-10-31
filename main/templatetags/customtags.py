from django import template

register = template.Library()

@register.filter()
def loop5cards(count,div):
    return int(count-1)%div