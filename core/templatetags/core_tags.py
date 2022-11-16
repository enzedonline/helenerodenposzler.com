import re

from django import template
from django.utils.safestring import mark_safe
from django.utils.text import normalize_newlines
from wagtail.admin.templatetags.wagtailadmin_tags import render_with_errors
from wagtail.models import Page

from site_settings.models import TemplateText

register = template.Library()


@register.simple_tag(takes_context=True)
def get_context_var_or_none(context, name):
    dicts = context.dicts  # array of dicts
    if dicts:
        for d in dicts:
            if name in d:
                return d[name]
    return None


@register.filter()
def strip_newlines(text):
    return re.sub(" +", " ", normalize_newlines(text).replace("\n", " "))


@register.filter()
def replace_doublequotes(text):
    return text.replace('"', "'")


@register.simple_tag()
def trans_url(link):
    return link.localized.url


@register.simple_tag()
def get_template_set(set):
    try:
        template_set = TemplateText.objects.filter(template_set=set).first()
        if template_set:
            items = template_set.localized.templatetext_items.all()
            if items:
                text_dict = {}
                for i in items:
                    text_dict[i.template_tag] = i.text
                return text_dict
        return TemplateText.objects.none()

    except (AttributeError, TemplateText.DoesNotExist):
        return TemplateText.objects.none()


@register.simple_tag()
def regex_render_with_errors(bound_field):
    id = bound_field.auto_id
    rendered_field = render_with_errors(bound_field)
    if f'id="{id}"' in rendered_field:
        script = f' onkeydown="return regex_keydownhandler(event)">\
        <script>function regex_keydownhandler(event) \
            {{if (!(/{bound_field.field.pattern}/.test(event.key))){{\
                return false;}} }} \
        </script>'       
        return mark_safe(rendered_field.replace('>', script))
    return rendered_field

@register.simple_tag(takes_context=True)
def var_exists(context, name):
    dicts = context.dicts  # array of dicts
    if dicts:
        for d in dicts:
            if name in d:
                return True
    return False


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
