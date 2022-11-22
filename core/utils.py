from urllib.parse import urlencode
from urllib.request import urlopen

from django.urls import reverse

PING_URL = "https://www.google.com/webmasters/tools/ping"


def ping_google(request, ping_url=PING_URL):
    try:
        sitemap = request.build_absolute_uri(reverse('sitemap'))
        params = urlencode({"sitemap": sitemap})
        urlopen(f"{ping_url}?{params}")
    except Exception as e:
        print(f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}")         