from django.conf import settings
from wagtail import hooks

from core.utils import ping_google

from .draftail_extensions import DRAFTAIL_ICONS, register_inline_styling
from .thumbnails import ThumbnailOperation


@hooks.register('register_image_operations')
def register_image_operations():
    return [
        ('thumbnail', ThumbnailOperation)
    ]

@hooks.register("register_rich_text_features")
def register_smaller_styling(features):
    register_inline_styling(
        features=features,
        feature_name='smaller',
        type_='SMALLER',
        tag='span',
        format='style="font-size:smaller;"',
        editor_style={'font-size':'smaller'},
        description='Decrease Font',
        icon=DRAFTAIL_ICONS.decrease_font
    )

@hooks.register("register_rich_text_features")
def register_larger_styling(features):
    register_inline_styling(
        features=features,
        feature_name='larger',
        type_='LARGER',
        tag='span',
        format='style="font-size:larger;"',
        editor_style={'font-size':'larger'},
        description='Increase Font',
        icon=DRAFTAIL_ICONS.increase_font
    )

@hooks.register("register_rich_text_features")
def register_underline_styling(features):
    register_inline_styling(
        features=features,
        feature_name='underline',
        type_='UNDERLINE',
        tag='u',
        description='Underline',
        icon=DRAFTAIL_ICONS.underline
    )

@hooks.register("after_publish_page")
def register_ping_google_after_publish(request, page):
    if not settings.DEBUG:
        ping_google(request)

@hooks.register("after_delete_page")
def register_ping_google_after_delete(request, page):
    if not settings.DEBUG:
        ping_google(request)
