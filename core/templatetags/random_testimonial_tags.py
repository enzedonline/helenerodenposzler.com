from django import template
from random import randint
from site_settings.models import Testimonial

register = template.Library()

@register.simple_tag()
def get_random_testimonial():
    count = Testimonial.objects.all().filter(locale_id=1).count()
    return Testimonial.objects.all().filter(locale_id=1)[randint(0, count - 1)].localized
