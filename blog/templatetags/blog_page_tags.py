from django import template
from blog.models import BlogListingPage
from wagtail.images.models import Image

register = template.Library()

@register.simple_tag()
def get_blog_index():
    blog_list_page = BlogListingPage.objects.all().first().localized
    return blog_list_page

@register.simple_tag()
def get_prev_next(page):
    prev = page.get_prev_siblings().live().first()
    next = page.get_next_siblings().live().first()
    next_icon = Image.objects.all().filter(title='blog-page-next-arrow').first()
    prev_icon = Image.objects.all().filter(title='blog-page-prev-arrow').first()
    return {'prev': prev, 'prev_icon': prev_icon,'next': next, 'next_icon': next_icon}