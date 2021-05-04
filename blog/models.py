from core.blocks import GridStreamBlock
from core.models import SEOPage
from django import forms
from django.utils.text import slugify
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django_extensions.db.fields import AutoSlugField
from modelcluster.fields import ParentalManyToManyField
from wagtail.admin.edit_handlers import (FieldPanel, MultiFieldPanel,
                                         StreamFieldPanel)
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.fields import StreamField
from wagtail.core.models import Locale, TranslatableMixin
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet


@register_snippet
class BlogCategory(TranslatableMixin, models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(
        blank=True,
        help_text=_("Set automatically"),
    )
    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
    ]

    class Meta:
        verbose_name = 'Blog Category'
        verbose_name_plural = 'Blog Categories'
        ordering = ['name']
        unique_together = ('translation_key', 'locale')
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(BlogCategory, self).save(*args, **kwargs)

class BlogDetailPage(SEOPage):
    template = "blog/blog_page.html"
    subpage_types = []
    parent_page_types = ['blog.BlogListingPage']

    body = StreamField(
        GridStreamBlock(), verbose_name="Page body", blank=True
    )
    categories = ParentalManyToManyField(
        'blog.BlogCategory',
    )

    content_panels = SEOPage.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel(
                    'categories', 
                    widget = forms.CheckboxSelectMultiple,
                ),
            ],
            heading = "Blog Categories",
        ),
        StreamFieldPanel("body"),
    ]

    class Meta:
        verbose_name = _("Blog Page")

class BlogListingPage(RoutablePageMixin, SEOPage):
    template = "blog/blog_index_page.html"
    parent_page_types = ['home.HomePage']
    subpage_types = [
        "blog.BlogDetailPage", 
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

    top_section = StreamField(
        GridStreamBlock(), 
        verbose_name="Content to go above the index", 
        blank=True
    )
    bottom_section = StreamField(
        GridStreamBlock(), 
        verbose_name="Content to go below the index", 
        blank=True
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
        StreamFieldPanel("top_section"),
        StreamFieldPanel("bottom_section"),
    ]

    # def get_context(self, request, *args, **kwargs):
    #     """Adds custom fields to the context"""
    #     context = super().get_context(request, *args, **kwargs)
    #     context['posts'] = BlogDetailPage.objects.child_of(self).live().public().reverse()
    #     return context

    @property
    def get_child_pages(self):
        return self.get_children().public().live()

    def get_context(self, request, *args, **kwargs):
        """Adds custom fields to the context"""
        context = super().get_context(request, *args, **kwargs)
        # all_posts = self.get_children().public().live().order_by('-first_published_at')
        all_posts = BlogDetailPage.objects.child_of(self).live().public().reverse()
        
        categories = BlogCategory.objects.all().filter(locale_id=Locale.get_active().id)
        category_filter = request.GET.get("category", None)
        if category_filter:
            # distinct not supported in sqlite
            # all_posts = all_posts.filter(categories__slug__in=[category_filter]).distinct('id')
            all_posts = all_posts.filter(categories__slug__in=category_filter.split(','))
            verbose_category_list = ""
            for item in category_filter.split(','):
                try:
                    verbose_category_list += "'" + categories.filter(slug=item).first().name + "' "
                except BlogCategory.DoesNotExist:
                    verbose_category_list += "'" + item + "' "
            context['category_filter'] = verbose_category_list

#         tag_filter = request.GET.get("tag", None)
#         if tag_filter:
#             # distinct not supported in sqlite
# #            all_posts = all_posts.filter(tags__slug__in=['tag1','tag2']).distinct('id')
#             all_posts = all_posts.filter(tags__slug__in=tag_filter.split(','))
#             verbose_tag_list = ""
#             for item in tag_filter.split(','):
#                 try:
#                     verbose_tag_list += "'" + Tag.objects.get(slug=item).name + "' "
#                 except Tag.DoesNotExist:
#                     verbose_tag_list += "'" + item + "' "
#             context['tag_filter'] = verbose_tag_list

        paginator = Paginator(all_posts, 8)

        requested_page = request.GET.get("page")

        try:
            posts = paginator.page(requested_page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        
        context['page_range'] = paginator_range(
            requested_page=posts.number,
            last_page_num=paginator.num_pages,
            wing_size=4
        )
        # Next two are needed as Django templates don't support accessing range properties
        context['page_range_first'] = context['page_range'][0]
        context['page_range_last'] = context['page_range'][-1]
        context["posts"] = posts
        context['categories'] = categories

        return context

    @route(r"^category/$", name="category_list")
    @route(r"^category/(?P<cat_slug>[-\w]*)/$", name="category_view")
    def category_view(self, request, cat_slug=None):
        context = self.get_context(request)
        try:
            # Look for the blog category by its slug.
            category = BlogCategory.objects.get(slug=cat_slug)
            context["posts"] = BlogDetailPage.objects.child_of(self).live().public().filter(categories__in=[category]).reverse()
            context['category_filter'] = category.name
        except Exception:
            # Blog category doesnt exist (ie /blog/category/missing-category/)
            category = None

        if category is None:
            context['categories'] = BlogCategory.objects.all().filter(locale_id=Locale.get_active().id).order_by('name')
            return render(request, "blog/category_list.html", context)  

        return render(request, "blog/blog_index_page.html", context)            


def paginator_range(requested_page, last_page_num, wing_size=5):
    """ Given a 'wing size', return a range for pagination. 
        Wing size is the number of pages that flank either side of the selected page
        Presuming missing pages will be denoted by an elipse '...', 
        the minimum width is 2xelipse + 2x wing size + selcted page
        if the elipse is one off the outer limit, replace it with the outer limit
        The range returned will always return a fixed number of boxes to the properly configured pagination nav"""

    # If last page number is within minimum size, just return entire range
    if last_page_num <= ((2 * (wing_size + 1)) + 1):
        return range(1, last_page_num + 1)

    # find the start page or return 1 if within wing range
    start_page = max([requested_page - wing_size, 1])

    if start_page == 1:
        # first elipse is 1, add one to the end and also one for the selected page (also 1 in this case) 
        end_page = (2 * wing_size) + 2
    else:
        # return range end or last page if over that
        end_page = min([requested_page + wing_size, last_page_num])
        if end_page == last_page_num:
            # last elipse is taken by last page number, start is twice the wing plus 1 for the selected page 
            # and 1 for the replaced elipse
            start_page = last_page_num - ((2 * wing_size) + 1)

    # if the ends are within one place of the end points, replace with the actual end point
    # otherwise it's just an elipse where the endpoint would be ... pointless
    if start_page == 2:
        start_page = 1 
    if end_page == last_page_num - 1:
        end_page = last_page_num
    return range(start_page, end_page + 1)
