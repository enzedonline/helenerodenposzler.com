from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.fields import RichTextField
from wagtail.models import Locale, Orderable, TranslatableMixin
from wagtail.snippets.models import register_snippet
from wagtail_localize.fields import SynchronizedField, TranslatableField

from core.edit_handlers import RegexPanel, ServiceTypeFieldPanel


class PasswordField(forms.CharField):
    widget = forms.PasswordInput

class PasswordModelField(models.CharField):

    def formfield(self, **kwargs):
        defaults = {'form_class': PasswordField}
        defaults.update(kwargs)
        return super(PasswordModelField, self).formfield(**defaults)

@register_setting(icon='mail')
class EmailSettings(BaseSetting):
    default_from_email = models.CharField(
        max_length=80,
        null=True,
        blank=False,
        verbose_name=_("Sending Email Address")
    )
    host = models.CharField(
        max_length=80,
        null=True,
        blank=False,
        verbose_name=_("Mail Server")
    )
    port = models.IntegerField(
        null=True,
        blank=False,
        verbose_name=_("Port")
    )
    username = models.CharField(
        max_length=50,
        null=True,
        blank=False,
        verbose_name=_("Username")
    )
    password = PasswordModelField(
        max_length=30,
        null=True,
        blank=False,
        verbose_name=_("Password"),
    )
    use_tls = models.BooleanField(
        default=False,
        verbose_name=_("Use TLS"),
        help_text=_("Use only TLS or SSL")
    )
    use_ssl = models.BooleanField(
        default=True,
        verbose_name=_("Use SSL"),
        help_text=_("Use only TLS or SSL")
    )

@register_snippet
class SocialMedia(TranslatableMixin, models.Model):

    site_name = models.CharField(
        max_length=30,
        null=False,
        blank=False,
        help_text=_("Site Name")
    )
    url = models.URLField(
        max_length=100,
        null=False,
        blank=False,
        help_text=_("Profile URL")
    )
    photo = models.ForeignKey(
        "wagtailimages.Image",
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text=_("Social Media Icon (displayed at 25x25)")
    )
 
    panels = [
        FieldPanel('site_name'),
        FieldPanel('url'),
        FieldPanel('photo'),
    ]
    override_translatable_fields = [
        SynchronizedField("photo", overridable=True),
    ]   
    
    def __str__(self):
        """The string representation of this class"""
        return self.site_name

    class Meta:
        verbose_name = 'Social Media Link'
        verbose_name_plural = 'Social Media Links'
        unique_together = ('translation_key', 'locale')

@register_snippet
class EmailSignature(TranslatableMixin, models.Model):
    signature_name = models.CharField(
        max_length=30,
        null=False,
        blank=False,
        verbose_name=_("Email Signature Title"),
        help_text=_("Used to identify this signature")
    )
    signature_content = RichTextField(
        features= [
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            'bold',
            'italic',
            'ol',
            'ul',
            'link',
            'hr',
        ],
        verbose_name=_("Email Signature Content"),
        help_text=_("Text for the Email Signature")
    )
    signature_image = models.ForeignKey(
        'wagtailimages.Image',
        blank=True,
        null=True,
        related_name='+',
        on_delete=models.SET_NULL,
        verbose_name=_("Image for Left Column"),
        help_text=_("Image to display in left column of Email Signature")
    )

    panels = [
        FieldPanel('signature_name'),
        FieldPanel('signature_content'),
        FieldPanel('signature_image'),
    ]

    def __str__(self):
        """The string representation of this class"""
        return self.signature_name

    class Meta:
        verbose_name = _('Email Signature')
        verbose_name_plural = _('Email Signatures')
        unique_together = ('translation_key', 'locale')

@register_snippet
class Organisation(TranslatableMixin, models.Model):
    name = models.CharField(max_length=250)
    locality = models.CharField(max_length=250)
    region = models.CharField(max_length=250)
    country_code = models.CharField(max_length=2)
    logo = models.ForeignKey(
        "wagtailimages.Image", on_delete=models.CASCADE, related_name="+"
    )
    image = models.ForeignKey(
        "wagtailimages.Image", on_delete=models.CASCADE, related_name="+",
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("logo"),
        FieldPanel("image"),
        FieldPanel("locality"),
        FieldPanel("region"),
        FieldPanel("country_code"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('translation_key', 'locale')

@register_snippet
class ServiceType(TranslatableMixin, ClusterableModel):
    """Types of services offered"""
    service = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        help_text=_("Service Type")
    )

    panels = [
        FieldPanel("service"),
        MultiFieldPanel(
            [
                InlinePanel("service_offerings"),
            ],
            heading=_("Service Offerings"),
        ),
    ]

    def __str__(self):
        return self.service

class ServiceOffering(TranslatableMixin, Orderable):
    service_type = ParentalKey(
        "ServiceType",
        related_name="service_offerings"
    )
    description = models.TextField(
        null=True,
        blank=False
    )

    panels = [
        FieldPanel('description'),
    ]

    def __str__(self):
        return self.description

    class Meta:
        unique_together = ('translation_key', 'locale')


class ServiceListQuerySet(object):
    # Call as class()() to act as a function call, passes service list to ServiceTypePanel dropdown
    def __call__(self, *args, **kwds):
        return ServiceType.objects.all()

@register_snippet
class Testimonial(TranslatableMixin, models.Model):
    """Testimonial Class"""

    reference_text = models.TextField(
        max_length=800,
        null=False,
        blank=False,
        help_text=_("Reference text")
    )
    author = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        help_text=_("Name of referee")
    )
    author_description = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        help_text=_("Optional - Brief description of referee ('Mother of a student' etc)")
    )
    photo = models.ForeignKey(
        "wagtailimages.Image",
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text=_("Photo of author (displayed at 25x25)")
    )
    service = models.ForeignKey(
        ServiceType, on_delete=models.SET_NULL,
        blank=False,
        null=True,
    )
    author_link = models.URLField(
        max_length=100,
        null=True,
        blank=True,
        help_text=_("Optional link to testimonial author")
    )

    panels = [
        FieldPanel('author'),
        FieldPanel('author_description'),
        FieldPanel('reference_text'),
        FieldPanel('photo'),
        FieldPanel('author_link'),
        ServiceTypeFieldPanel('service', ServiceListQuerySet()()),
    ]

    override_translatable_fields = [
        SynchronizedField("photo", overridable=False),
        SynchronizedField("author_link", overridable=False),
        SynchronizedField("service", overridable=False),
    ]   

    def __str__(self):
        """The string representation of this class"""
        return self.author

    class Meta:
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonials'
        unique_together = ('translation_key', 'locale')

@register_snippet
class TemplateText(TranslatableMixin, ClusterableModel):
    template_set = models.CharField(
        # unique=True,
        max_length=50,
        verbose_name="Set Name",
        help_text=_("The set needs to be loaded in template tags then text references as {{set.tag}}")
    )    

    translatable_fields = [
        TranslatableField('templatetext_items'),
    ]    

    panels = [
        FieldPanel("template_set"),
        MultiFieldPanel(
            [
                InlinePanel("templatetext_items"),
            ],
            heading=_("Text Items"),
        ),
    ]

    def __str__(self):
        return self.template_set
    
    class Meta:
        verbose_name = _('Template Text')
        unique_together = ('translation_key', 'locale'), ('locale', 'template_set')

    def clean(self):
        # Check unique_together constraint
        # Stop instances being created outside of default locale
        # ASSUMPTION: the field in the unique_together (template_set) is non-translatable

        def_lang = Locale.get_default()
        
        if self.locale==Locale.get_default():
            # If in default locale, look for other sets with the template_set value (checking pre-save value)
            # Exclude other locales (will be translations of current locale)
            # Exclude self to cater for editing existing instance. Name change still checked against other instances.
            if TemplateText.objects.filter(template_set=self.template_set).filter(locale=self.locale_id).exclude(pk=self.pk).count()>0:
                raise ValidationError(_("This template set name is already in use. Please only use a unique name."))
        elif self.get_translations().count()==0:
            # If not in default locale and has no translations, new instance being created outside of default, raise error
            raise ValidationError(_(f"Template sets can only be created in the default language ({def_lang}). \
                                      Please create the set in {def_lang} and use the translate option."))

    def delete(self):
        # If deleting instance in default locale, delete translations
        # Remove if clause if using multi-level translations (eg EN > ES > CA)
        if self.locale==Locale.get_default():
            for trans in self.get_translations():
                trans.delete()
        super().delete()

class TemplateTextSetItem(TranslatableMixin, Orderable):
    set = ParentalKey(
        "TemplateText",
        related_name="templatetext_items",
        help_text=_("Template Set to which this item belongs."),
        verbose_name="Set Name",
    )
    template_tag = models.SlugField(
        max_length=50,
        help_text=_("Enter a tag without spaces, consisting of letters, numbers, underscores or hyphens."),
        verbose_name="Template Tag",
    )    
    text = models.TextField(
        null=True,
        blank=True,
        help_text=_("The text to be inserted in the template.")
    )

    translatable_fields = [
        TranslatableField('text'),
    ]

    panels = [
        RegexPanel(field_name='template_tag', pattern='^[-\w]+$'),
        FieldPanel('text'),
    ]

    def __str__(self):
        return self.template_tag

    class Meta:
        unique_together = ('set', 'template_tag'), ('translation_key', 'locale')
