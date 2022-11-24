from site_settings.models import SocialMedia
from menu.models import Menu
from django import template
from django.templatetags.static import static
from wagtail.models import Page, Locale
from wagtail.images.models import Image

def sub_menu_items(menu, logged_in):
    # return any submenus for the menu instance
    sub_menu_items = []
    for item in menu.sub_menu_items.all():
        if item.show(logged_in):
            sub_menu_items.append({
                'order': item.menu_display_order,
                'submenu_id': item.submenu_id, 
                'is_submenu': True,
                'divider': item.show_divider_after_this_item,
                'display_option': item.display_option,
            })
    return sub_menu_items

def link_menu_items(menu, logged_in):
    #return any links for the menu instance
    link_menu_items = []
    for item in menu.link_menu_items.all():
        if item.show(logged_in): # authentication status of user matches item 'show_when' property
            if item.link_page: # link is to internal page (not url)
                trans_page = item.link_page.localized # get translated page if any
                if not item.title: # no title set in menu item, use page title
                    item.title = trans_page.title
                url = str(trans_page.url)
                if item.link_url: # anything in url field to be treated as suffix (eg /?cat=news)
                    url = url + str(item.link_url)
            else: # not a page link, test if internal or external url, translate if internal
                if item.link_url.startswith('/'): # presumes internal link starts with '/' and no lang code
                    url = '/' + Locale.get_active().language_code + item.link_url
                else: # external link, do nothing
                    url = item.link_url                
            link_menu_items.append({
                'order': item.menu_display_order,
                'title': item.title, 
                'url': url,
                'icon': item.icon,
                'is_submenu': False,
                'divider': item.show_divider_after_this_item,
            })
    return link_menu_items

def autofill_menu_items(menu, logged_in):
    autofill_menu_items = []
    for item in menu.autofill_menu_items.all():
        if item.show(logged_in): # authentication status of user matches item 'show_when' property
            trans_page = item.link_page.localized # get translated page if any
            if trans_page:
                if item.include_linked_page: # show linked page as well as any results
                    autofill_menu_items.append({
                        'order': item.menu_display_order,
                        'title': trans_page.title, 
                        'url': trans_page.url,
                        'is_submenu': False,
                        'divider': True,
                    })
                # return only public pages if user not logged in
                if logged_in:
                    list = trans_page.get_children().live().order_by(item.order_by)
                else:
                    list = trans_page.get_children().live().public().order_by(item.order_by)
                # filter by 'Show In Menu' if selected
                if item.only_show_in_menus:
                    list = list.filter(show_in_menus=True)
                # limit list to maximum set in menu item
                list = list[:item.max_items]
                # add results (if any) to menu items
                if list:
                    i = 0
                    for result in list:
                        autofill_menu_items.append({
                            'order': item.menu_display_order + i/(item.max_items + 1),
                            'title': result.title, 
                            'url': result.url,
                            'is_submenu': False,                            
                        })
                        i+=1
                    # if add divider selected, add to last item only
                    autofill_menu_items[-1]['divider'] = item.show_divider_after_this_item
    return autofill_menu_items

register = template.Library()

@register.simple_tag()
def get_menu_items(menu, request):
    # returns a list of dictionaries with title, url, page and icon of all items in the menu
    # use get_menu first to load the menu object then pass that instance to this function

    if not request: # 500 error has no request
        authenticated = False
    else:
        authenticated = request.user.is_authenticated

    if not isinstance(menu, Menu):
        if isinstance(menu, int):
            # menu id supplied instead of menu instance
            menu = get_menu(menu)
        if menu == None:
            # couldn't load menu, return nothing
            return None
    
    # gather all menu item types, sort by menu_display_order at the end
    # create a list of all items that should be shown in the menu depending on logged_in
    menu_items = [] + \
                 sub_menu_items(menu, authenticated) + \
                 link_menu_items(menu, authenticated) + \
                 autofill_menu_items(menu, authenticated)

    # if no menu items to show, return None
    if menu_items.__len__() == 0:
        return None

    # sort menu items by common 'order' field
    menu_items = sorted(menu_items, key=lambda k: k['order'])

    return menu_items

@register.simple_tag()
def get_menu(menu_title):
    # return the localized menu instance for a given title, or none if no such menu exists
    try:
        if isinstance(menu_title, int):
            return Menu.objects.all().filter(id=menu_title).first().localized 
        else:
            return Menu.objects.all().filter(title=menu_title).first().localized 
    except (AttributeError, Menu.DoesNotExist):
        return None
    
@register.simple_tag()
def language_switcher(page):
    # Build the language switcher
    # determine next_url for each locale if page has translation
    # /lang/<lang-code> redirects to menu.views.set_language_from_url:
    #     path('lang/<str:language_code>/', set_language_from_url),
    # if no ?next= param passed to the view, it will attempt to determine best url from HTTP_REFERER
    # this will happen if non-Wagtail page is served, or if Wagtail page has no translation

    current_lang = Locale.get_active()
    switcher = []

    for locale in Locale.objects.all():
        # page will be None if non-Wagtail page served
        next_url = ''
        try:
            trans_page = page.get_translation_or_none(locale=locale)
            # if page has live translation forward to that page, else forward to home page in new locale
            next_url = f'?next={trans_page.url}' if trans_page and trans_page.live else '?next=/'
        except AttributeError: # non-Wagtail page, let view determine best url to forward to
            next_url = ''

        if not locale == current_lang: # add the link to switch language 
            flag = get_lang_flag(locale)
            switcher.append(
                {
                    'language': flag['language'], 
                    'url': f'/lang/{locale.language_code}/{next_url}',
                    'flag': flag['image']
                }
            )

    return switcher

@register.simple_tag()
def get_lang_flag(locale=None):
    # returns the flag icon for the menu 
    # upload flag svg image to static/svg/flags, filename must match locale code (ie fr.svg en-gb.svg etc)
    # if no language code supplied, assumes current language
    if not locale:
        locale = Locale.get_active()
    return {
        'image': f"{static('/svg/flags')}/{locale.language_code}.svg",
        'language': locale.get_display_name()
    }

@register.simple_tag()
def get_social_media_icons():
    try:
        social_media_icons = []
        icons = SocialMedia.objects.all().filter(locale_id=1)
        for icon in icons:
            item = {}
            locale_icon = icon.localized
            item['link'] = locale_icon.url
            item['image'] = locale_icon.photo.get_rendition('fill-25x25').url
            item['alt'] = locale_icon.site_name
            social_media_icons.append(item)
        return social_media_icons
    except:
        return None

    