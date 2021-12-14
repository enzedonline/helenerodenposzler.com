from django import template
from django.utils.safestring import mark_safe
from wagtail.core.models import Page

register = template.Library()


@register.simple_tag()
def trans_url(link):
    return link.localized.url


@register.simple_tag(takes_context=True)
def robots(context):
    page = get_context_var_or_none(context, "self")
    if not page:
        return mark_safe('<meta name="robots" content="noindex">')
    return mark_safe(
        '<meta name="robots" content="index, follow, archive, imageindex, odp, snippet, translate, max-snippet:-1, max-image-preview:large, max-video-preview:-1" />'
    )

@register.simple_tag(takes_context=True)
def get_context_var_or_none(context, name):
    dicts = context.dicts  # array of dicts
    if dicts:
        for d in dicts:
            if name in d:
                return d[name]
    return None

@register.simple_tag
def print_template_value(value):
    print(value)

@register.simple_tag()
def trans_page_from_slug(slug, specific=False):
    try:
        if specific:
            return Page.objects.live().filter(slug=slug).first().specific.localized
        else:
            return Page.objects.live().filter(slug=slug).first().localized
    except:
        return Page.objects.none()
