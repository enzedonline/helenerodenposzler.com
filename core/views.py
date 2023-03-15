import os
from datetime import datetime

from django.template.response import TemplateResponse
from django.utils.http import http_date
from django.views.generic import TemplateView
from wagtail.models import Page, Site

env = os.environ.copy()


class RobotsView(TemplateView):

    content_type = "text/plain"

    def get_template_names(self):
        return "robots.txt"


def sitemap(request):
    site = Site.find_for_request(request)
    root_page = Page.objects.defer_streamfields().get(id=site.root_page_id)
    urlset = []
    for locale_home in (
        root_page.get_translations(inclusive=True)
        .live()
        .defer_streamfields()
        .specific()
    ):
        if locale_home.search_engine_index:
            urlset.append(locale_home.sitemap_urls)
        for child_page in (
            locale_home.get_descendants().live().defer_streamfields().specific()
        ):
            if child_page.search_engine_index:
                urlset.append(child_page.sitemap_urls)
    try:
        urlset.remove([])
    except:
        pass
    try:
        last_modified = max([x["lastmod"] for x in urlset])
    except Exception as e:
        # either urlset is empty or lastmod fields not present, set last modified to now
        print(
            f"\n{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}\n"
        )
        last_modified = datetime.now()

    return TemplateResponse(
        request,
        template="sitemap.xml",
        context={"urlset": urlset},
        content_type="application/xml",
        headers={
            "X-Robots-Tag": "noindex, noodp, noarchive",
            "last-modified": http_date(last_modified.timestamp()),
            "vary": "Accept-Encoding",
        },
    )
