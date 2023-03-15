from django.conf import settings
from django.db import models
from django.forms.widgets import CheckboxSelectMultiple
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalManyToManyField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.models import Page, Locale
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

    search_engine_index = models.BooleanField(
        blank=False,
        null=False,
        default=True,
        verbose_name=_("Allow search engines to index this page?")
    )

    search_engine_changefreq = models.CharField(
        max_length=25,
        choices=[
            ("always", _("Always")),
            ("hourly", _("Hourly")),
            ("daily", _("Daily")),
            ("weekly", _("Weekly")),
            ("monthly", _("Monthly")),
            ("yearly", _("Yearly")),
            ("never", _("Never")),
        ],
        blank=True,
        null=True,
        verbose_name=_("Search Engine Change Frequency (Optional)"),
        help_text=_("How frequently the page is likely to change? (Leave blank for default)")
    )

    search_engine_priority = models.DecimalField(
        max_digits=2, 
        decimal_places=1,
        blank=True,
        null=True,
        verbose_name=_("Search Engine Priority (Optional)"),
        help_text=_("The priority of this URL relative to other URLs on your site. Valid values range from 0.0 to 1.0. (Leave blank for default)")
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
        ], _('Common page configuration')),
        MultiFieldPanel([
            FieldPanel('page_type'),
            LocalizedSelectPanel(
                'services', 
                widget_class=CheckboxSelectMultiple, 
                ),
        ], _("Structured Data")),
        MultiFieldPanel([
            FieldPanel('search_engine_index'),
            FieldPanel('search_engine_changefreq'),
            FieldPanel('search_engine_priority'),
        ], _("Search Engine Indexing")),
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

    @property
    def alternates(self):
        default_locale = Locale.get_default()
        x_default = None

        trans_pages = self.get_translations(inclusive=True)
        if trans_pages.count() > 1:
            alt = []
            for page in trans_pages:
                alt.append({
                    'lang_code': page.locale.language_code,
                    'location': page.full_url
                })
                if page.locale == default_locale:
                    x_default = page.full_url
            
            if not x_default: # page not translated to default language, use first trans_page instead
                x_default = trans_pages.first().full_url
            alt.append({'lang_code': 'x-default', 'location': x_default})

            return alt
        else:
            return None

    @property
    def sitemap_urls(self):
        url_item = {
            "location": self.full_url,
            "lastmod": self.last_published_at or self.latest_revision_created_at,
            "alternates": self.alternates
        }
        if self.search_engine_changefreq:
            url_item["changefreq"] = self.search_engine_changefreq
        if self.search_engine_priority:
            url_item["priority"] = self.search_engine_priority
        
        return url_item

    class Meta:
        abstract = True

class SEOWagtailCaptchaEmailForm(SEOPage, WagtailCaptchaEmailForm):
    pass

    class Meta:
        abstract = True

