from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path, re_path
from menu.views import set_language_from_url
from search import views as search_views
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.contrib.sitemaps.views import sitemap
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from core.views import RobotsView
from django.views import defaults as default_views

def trigger_error(request):
    division_by_zero = 1 / 0
    
urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    re_path(r'^robots\.txt$', RobotsView.as_view(), name='robots'),
    re_path(r'^sitemap.xml$', sitemap),
    path('sentry-debug/', trigger_error),
    path('lang/<str:language_code>/', set_language_from_url, name='set_language_from_url'),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# These paths are translatable so will be given a language prefix (eg, '/en', '/fr')
urlpatterns = urlpatterns + i18n_patterns(
    path('search/', search_views.search, name='search'),
    re_path(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception("Permission Denied")}),
    re_path(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception("Page not Found")}),
    re_path(r'^500/$', default_views.server_error),    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
)
