from django.utils.translation import gettext_lazy as _
from django.db import models
from wagtail_blocks.blocks import *
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel, PageChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel

from core.blocks import GridStreamBlock
from core.models import SEOPage

class ServicePage(SEOPage):
    max_count = 5

    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        blank=False,
        null=True,
        related_name='+',
        on_delete=models.SET_NULL,
    )
    banner_headline = models.CharField(
        max_length=30,
        blank=True,
        null=True,
    )
    banner_small_text = models.CharField(
        max_length=60,
        blank=True,
        null=True,
    )
    banner_call_to_action_button_text = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )
    banner_call_to_action_button_link = models.ForeignKey(
        'wagtailcore.Page',
        blank=True,
        null=True,
        related_name="+",
        help_text='Select an optional page to link to',
        on_delete=models.SET_NULL,
    )

    body = StreamField(
        GridStreamBlock(), verbose_name="Page body", blank=True
    )

    content_panels = SEOPage.content_panels + [
        MultiFieldPanel(
            [
                ImageChooserPanel('banner_image'),
                FieldPanel('banner_headline'),
                FieldPanel('banner_small_text'),
                FieldPanel('banner_call_to_action_button_text'),
                PageChooserPanel('banner_call_to_action_button_link'),
            ], 
            heading=_("Choose banner image and text/button overlay options.")
        ),
        StreamFieldPanel("body"),
    ]

    class Meta:
        verbose_name = "Service Page"