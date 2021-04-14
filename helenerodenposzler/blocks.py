from django.db import models

from wagtail.snippets.models import register_snippet

@register_snippet
class Testimonial(models.Model):
    """Testimonial Class"""

    quote = models.TextField(
        max_length=500,
        null=False,
        blank=False
    )
    attribution = models.CharField(
        max_length=60,
        null=False,
        blank=False
    )

    def __str__(self):
        """The string representation of this class"""
        return f"{self.quote} - {self.attribution}"

    class Meta:
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonials'