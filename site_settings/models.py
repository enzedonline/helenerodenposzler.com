from django.utils.translation import gettext_lazy as _
from django.db import models
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.core.models import TranslatableMixin

@register_snippet
class SocialMedia(TranslatableMixin, models.Model):

    site_name = models.CharField(
        max_length=30,
        null=False,
        blank=False,
        help_text=_("Site Name")
    )
    url = models.URLField(
        max_length=100,
        null=False,
        blank=False,
        help_text=_("Profile URL")
    )
    photo = models.ForeignKey(
        "wagtailimages.Image",
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text=_("Social Media Icon (displayed at 25x25)")
    )
 
    panels = [
        FieldPanel('site_name'),
        FieldPanel('url'),
        ImageChooserPanel('photo'),
    ]

    def __str__(self):
        """The string representation of this class"""
        return self.site_name

    class Meta:
        verbose_name = 'Social Media Link'
        verbose_name_plural = 'Social Media Links'
        unique_together = ('translation_key', 'locale')

