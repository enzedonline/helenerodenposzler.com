from django.utils.translation import gettext_lazy as _
from wagtail_blocks.blocks import *
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import StreamFieldPanel
from django.db import models
from wagtail.core.models import TranslatableMixin
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.snippets.models import register_snippet
from core.blocks import BaseStreamBlock

@register_snippet
class ServiceType(TranslatableMixin, models.Model):
    """Types of services offered"""
    service = models.TextField(
        max_length=500,
        null=False,
        blank=False,
        help_text=_("Service Type")
    )

    def __str__(self):
        return self.service
        
@register_snippet
class Testimonial(TranslatableMixin, models.Model):
    """Testimonial Class"""

    reference_text = models.TextField(
        max_length=500,
        null=False,
        blank=False,
        help_text=_("Reference text")
    )
    author = models.CharField(
        max_length=60,
        null=False,
        blank=False,
        help_text=_("Name of referee")
    )
    author_description = models.CharField(
        max_length=60,
        null=True,
        blank=True,
        help_text=_("Optional - Brief description of referee ('Mother of a student' etc)")
    )
    photo = models.ForeignKey(
        "wagtailimages.Image",
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text=_("Photo of author (displayed at 25x25)")
    )
    # service = models.IntegerField(
    #     null=False,
    #     blank=False,
    #     choices=(
    #         (0,)
    #     )
    # )
    author_link = models.URLField(
        max_length=100,
        null=True,
        blank=True,
        help_text=_("Optional link to testimonial author")
    )

    panels = [
        FieldPanel('author'),
        FieldPanel('author_description'),
        FieldPanel('reference_text'),
        ImageChooserPanel('photo'),
        FieldPanel('author_link')
    ]

    def __str__(self):
        """The string representation of this class"""
        return f"{self.author} - {self.reference_text}"

    class Meta:
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonials'
        unique_together = ('translation_key', 'locale')

class HomePage(Page):
    body = StreamField(
        BaseStreamBlock(), verbose_name="Page body", blank=True
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel("body", classname="Full"),
    ]