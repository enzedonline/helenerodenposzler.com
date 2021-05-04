from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.core.models import Page, TranslatableMixin
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet
from wagtailcaptcha.models import WagtailCaptchaEmailForm
from wagtailmetadata.models import WagtailImageMetadataMixin

from .edit_handlers import ServiceTypeFieldPanel


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

class ServiceListQuerySet(object):
    # Call as class()() to act as a function call, passes service list to ServiceTypePanel dropdown
    def __call__(self, *args, **kwds):
        return ServiceType.objects.all()

@register_snippet
class Testimonial(TranslatableMixin, models.Model):
    """Testimonial Class"""

    reference_text = models.TextField(
        max_length=800,
        null=False,
        blank=False,
        help_text=_("Reference text")
    )
    author = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        help_text=_("Name of referee")
    )
    author_description = models.CharField(
        max_length=150,
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
    service = models.ForeignKey(
        ServiceType, on_delete=models.SET_NULL,
        blank=False,
        null=True,
    )
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
        FieldPanel('author_link'),
        ServiceTypeFieldPanel('service', ServiceListQuerySet()()),
    ]

    def __str__(self):
        """The string representation of this class"""
        return self.author

    class Meta:
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonials'
        unique_together = ('translation_key', 'locale')

def get_image_model_string():
    try:
        image_model = settings.WAGTAILIMAGES_IMAGE_MODEL
    except AttributeError:
        image_model = 'wagtailimages.Image'
    return image_model

class SEOPageMixin(WagtailImageMetadataMixin, models.Model):
    """An implementation of MetadataMixin for Wagtail pages."""
    search_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=False,
        related_name='+',
        on_delete=models.SET_NULL,
        verbose_name=_('Search Image')
    )

    summary = models.TextField(
        null=False,
        blank=False,
        help_text=_("A summary of the page to be used on index pages. \
                     If Search Description is left blank, this text will be used on searh results and link previews.")
    )

    content_panels = Page.content_panels + [
        FieldPanel('summary'),
    ]
    
    promote_panels = [
        MultiFieldPanel([
            FieldPanel('slug'),
            FieldPanel('seo_title'),
            FieldPanel('show_in_menus'),
            FieldPanel('search_description'),
            ImageChooserPanel('search_image'),
        ], _('Common page configuration')),
    ]

    def get_meta_url(self):
        return self.full_url

    def get_meta_title(self):
        return self.seo_title or self.title

    def get_meta_description(self):
        return self.search_description or self.summary

    def get_meta_image(self):
        return self.search_image

    class Meta:
        abstract = True

class SEOPage(SEOPageMixin, Page):
    pass

    class Meta:
        abstract = True

class SEOWagtailCaptchaEmailForm(SEOPageMixin, WagtailCaptchaEmailForm):
    pass

    class Meta:
        abstract = True

