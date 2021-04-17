from django import template
from django.utils.translation import get_language_from_request

register = template.Library()

@register.simple_tag(takes_context=True)
def quote_marks(context):
    language = get_language_from_request(context.get('request', None))
    quote_mark = {}
    if language in ('fr', 'es'):
        quote_mark['open'] = "«"
        quote_mark['close'] = "»"
    else:
        quote_mark['open'] = "“"
        quote_mark['close'] = "”"

    return quote_mark
