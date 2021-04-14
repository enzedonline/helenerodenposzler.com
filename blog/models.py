from django.conf import settings
from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import Page, TranslatableMixin
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail_localize.synctree import Page as LocalizePage


class ImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    caption = blocks.CharBlock(required=False)

    class Meta:
        icon = 'image'

class StoryBlock(blocks.StreamBlock):
    heading = blocks.CharBlock()
    paragraph = blocks.RichTextBlock()
    image = ImageBlock()


@register_snippet
class BlogCategory(TranslatableMixin):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Blog Categories"
        unique_together = ('translation_key', 'locale')

class BlogPostPage(Page):
    template = "blog/blog_page.html"
    publication_date = models.DateField(null=True, blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True
    )
    body = StreamField(StoryBlock())
    category = models.ForeignKey(
        BlogCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name='blog_posts'
    )

    content_panels = Page.content_panels + [
        FieldPanel('publication_date'),
        ImageChooserPanel('image'),
        StreamFieldPanel('body'),
        SnippetChooserPanel('category'),
    ]

    parent_page_types = ['blog.BlogIndexPage']

    def get_context(self, request, *args, **kwargs):
        """Adds custom fields to the context"""
        context = super().get_context(request, *args, **kwargs)
        context['lang_versions'] = self.get_translations()
        context['default_lang'] = (settings.LANGUAGES[0][0])
        return context

class BlogIndexPage(LocalizePage):
    template = "blog/blog_index_page.html"
    introduction = models.TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('introduction'),
    ]

    parent_page_types = ['home.HomePage']

    def get_context(self, request, *args, **kwargs):
        """Adds custom fields to the context"""
        context = super().get_context(request, *args, **kwargs)
        context['posts'] = BlogPostPage.objects.child_of(self).live().public().reverse()
        context['lang_versions'] = self.get_translations()
        context['default_lang'] = (settings.LANGUAGES[0][0])
        return context