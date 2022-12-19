from django import template
from django.utils.safestring import mark_safe
from wagtail.models import Locale

from site_settings.models import SocialMedia, Organisation
from .core_tags import get_context_var_or_none

register = template.Library()

@register.simple_tag()
def organisation_name():
    organisation = Organisation.objects.first()
    return organisation.localized.name if organisation else ''
    
@register.simple_tag()
def get_google_thumbnails(img):
    try:
        return {
            'tn1x1': img.get_rendition('thumbnail-500x500|format-png'),
            'tn4x3': img.get_rendition('thumbnail-500x375|format-png'),
            'tn16x9': img.get_rendition('thumbnail-500x281|format-png'),
        }
    except:
        return {
            'tn1x1': '',
            'tn4x3': '',
            'tn16x9': '',
        }
            
@register.simple_tag()
def get_social_media_sameas():
    same_as = []
    for sm in SocialMedia.objects.all().filter(locale_id=Locale.get_default().id):
        same_as.append(f'"{sm.localized.url}"')
    return mark_safe(','.join(same_as))

@register.simple_tag()
def get_organisation():
    try:
        organisation = Organisation.objects.first().localized
        if organisation:
            return {
                'name': organisation.name,
                'logo': organisation.logo.get_rendition('thumbnail-500x500|format-png').full_url,
                'thumbnails': get_organisation_thumbnails(organisation.image),
                'locality': organisation.locality,
                'region': organisation.region
            }
        else:
            return ''
                
    except (AttributeError, Organisation.DoesNotExist):
        return ''   

def get_organisation_thumbnails(img):
    return mark_safe(
        f"\"{img.get_rendition('thumbnail-500x500|format-png').full_url}\", "
        f"\"{img.get_rendition('thumbnail-500x375|format-png').full_url}\", "
        f"\"{img.get_rendition('thumbnail-500x281|format-png').full_url}\""
    )
    
@register.simple_tag(takes_context=True)
def get_local_business(context):
    page = get_context_var_or_none(context, 'self')
    if not page:
        return ''
    organisation = Organisation.objects.first().localized
    if not organisation:
        return ''
    org_logo = organisation.logo.get_rendition('thumbnail-500x500|format-png').full_url
    same_as = get_social_media_sameas()

    return mark_safe(
        f'{{'
        f'"@type": "LocalBusiness",'
        f'"@id": "{page.get_site().root_url}",'
        f'"name": "{organisation.name}",'
        f'"logo": "{org_logo}",'
        f'"image": [{get_organisation_thumbnails(organisation.image)}],'
        f'"url": "{page.get_site().root_url}",'
        f'"sameAs": [{same_as}],'
        f'"address": {get_organisation_address(organisation)}'
        f'}}'
    )

@register.simple_tag()
def get_organisation_address(organisation=None):
    if not organisation:
        organisation = Organisation.objects.first().localized

    return mark_safe(
        f'{{'
        f'"@type": "PostalAddress",'
        f'"addressLocality": "{organisation.locality}",'
        f'"addressRegion": "{organisation.region}",'
        f'"addressCountry": "{organisation.country_code}"'
        f'}}'
    )

@register.simple_tag()
def get_offerings(service):
    offerings = []
    for offering in service.service_offerings.all():
        offerings.append(f'{{"@type": "Offer","itemOffered": {{"@type": "Service","name": "{offering}"}}}}')
    return mark_safe(','.join(offerings))

@register.simple_tag(takes_context=True)
def get_services(context):
    page = get_context_var_or_none(context, 'self')
    if not page:
        return ''
    return page.get_translation(Locale.get_default().id).services.all()
     
