from django.conf import settings
from django.db import models
from django.forms.widgets import CheckboxSelectMultiple
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalManyToManyField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.models import Page
from wagtailcaptcha.models import WagtailCaptchaEmailForm
from wagtailmetadata.models import WagtailImageMetadataMixin

from core.edit_handlers import LocalizedSelectPanel


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

    page_type = models.CharField(
        max_length=25,
        choices=[
            ("WebPage", "Web Page"),
            ("AboutPage", "About Page"),
            ("ContactPage", "Contact Page"),
            ("ItemPage", "Item Page")
        ],
        default="WebPage",
        verbose_name=_("Structured Data Page Type")
    )

    services = ParentalManyToManyField(
        'site_settings.ServiceType',
        verbose_name=_("Services offered on this page"),
        blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('summary'),
    ]
    
    promote_panels = [
        MultiFieldPanel([
            FieldPanel('slug'),
            FieldPanel('search_image'),
            FieldPanel('seo_title'),
            FieldPanel('search_description'),
            FieldPanel('page_type'),
            MultiFieldPanel(
                [
                    LocalizedSelectPanel(
                        'services', 
                        widget_class=CheckboxSelectMultiple, 
                        ),
                ],
                heading = _("Services"),
            ),
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

