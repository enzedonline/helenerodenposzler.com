from django.utils.translation import gettext_lazy as _
from django.db import models
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail_localize.synctree import Locale, Page as LocalePage

from core.blocks import GridStreamBlock
from core.models import SEOPage

class HomePage(SEOPage):

    subpage_types = [
        "service.ServicePage", 
        "contact.ContactPage", 
        "blog.BlogListingPage",
    ]
    max_count = 1

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

    body = StreamField(
        GridStreamBlock(), verbose_name="Page body", blank=True
    )

    content_panels = SEOPage.content_panels + [
        MultiFieldPanel(
            [
                ImageChooserPanel('banner_image'),
                FieldPanel('banner_headline'),
                FieldPanel('banner_small_text'),
            ], 
            heading=_("Choose banner image and text/button overlay options.")
        ),
        StreamFieldPanel("body"),
    ]

    class Meta:
        verbose_name = "Home Page"

    def get_sitemap_urls(self, request):
        sitemap = super().get_sitemap_urls(request)

        for locale_home in self.get_siblings(inclusive=False).live():
            for entry in locale_home.get_sitemap_urls(request):
                sitemap.append(entry)
            for child_page in locale_home.get_descendants().live():
                for entry in child_page.get_sitemap_urls(request):
                    sitemap.append(entry)
        return sitemap        