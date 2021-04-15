from django.utils.translation import gettext_lazy as _
from wagtail_blocks.blocks import *
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import StreamFieldPanel

from core.blocks import BaseStreamBlock
from core.models import SEOPage

class HomePage(SEOPage):
    max_count = 1

    body = StreamField(
        BaseStreamBlock(), verbose_name="Page body", blank=True
    )

    content_panels = SEOPage.content_panels + [
        StreamFieldPanel("body", classname="Full"),
    ]

    class Meta:
        verbose_name = "Home Page"