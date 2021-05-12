from django.template.loader import render_to_string
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList
from wagtail.core.blocks.field_block import IntegerBlock, URLBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.core import blocks as wagtail_blocks
from wagtail.core.blocks import BooleanBlock, CharBlock, TextBlock, StreamBlock, StructBlock, RawHTMLBlock
from wagtail.core.blocks.stream_block import StreamValue
from wagtail_localize.synctree import Locale
from wagtail.core.fields import StreamField
from django.forms.widgets import Input
from django.db import models

class ColourThemeChoiceBlock(wagtail_blocks.ChoiceBlock):
    choices=[
        ('bg-transparent', _("Transparent")),
        ('text-black bg-light', _("Light")),
        ('text-white bg-dark', _("Dark")),
        ('text-black bg-helene-green', _("Green")),
        ('text-black bg-helene-faded-green', _("Faded Green")),
        ('text-black bg-helene-grey-green', _("Grey Green")),
        ('text-white bg-helene-coral', _("Coral")),
        ('text-white bg-helene-magenta', _("Magenta")),
        ('text-white bg-helene-blue', _("Blue")),
        ('text-white bg-helene-cerise', _("Cerise")),
        ('text-black bg-helene-moutard', _("Moutard")),
    ]

class ButtonChoiceBlock(wagtail_blocks.ChoiceBlock):
    choices=[
        ('btn-primary', _("Standard Button")),
        ('btn-btn-secondary', _("Secondary Button")),
        ('btn-link', _("Text Only")),
        ('btn-success', _("Success Button")),
        ('btn-danger', _("Danger Button")),
        ('btn-warning', _("Warning Button")),
        ('btn-info', _("Info Button")),
        ('btn-light', _("Light Button")),
        ('btn-dark', _("Dark Button")),
    ]

class ImageFormatChoiceBlock(wagtail_blocks.ChoiceBlock):
    choices=[
        ('4-1', _("4:1 Horizontal Letterbox Banner")),
        ('3-1', _("3:1 Horizontal Panorama Banner")),
        ('4-3', _("4:3 Horizontal Standard Format")),
        ('1-1', _("1:1 Square Format")),
        ('3-4', _("3:4 Portrait Standard Format")),
        ('1-3', _("1:3 Vertical Panorama Banner")),
    ]

class SEOImageChooseBlock(StructBlock):
    file = ImageChooserBlock(required=True, label=_("Image"))
    seo_title = CharBlock(
        required=True,
        label=_("SEO Title")
    )

class ImageBlock(StructBlock):
    """
    Custom `StructBlock` for utilizing images with associated caption and
    attribution data
    """
    image = SEOImageChooseBlock(required=True, label=_("Select Image & Enter Details"))
    caption = CharBlock(required=False, label=_("Image Caption (optional)"))
    attribution = CharBlock(required=False, label=_("Image Attribution (optional)"))
    background = ColourThemeChoiceBlock(
        default='bg-transparent',
        label=_("Card Background Colour")
    )
    class Meta:
        icon = 'image'
        template = "blocks/image_block.html"

class BlockQuote(StructBlock):
    """
    Custom `StructBlock` that allows the user to attribute a quote to the author
    """
    text = TextBlock(label=_("Quote"))
    attribute_name = CharBlock(
        blank=True, required=False, label=_("Optional Attribution"))
    background = ColourThemeChoiceBlock(
        default='bg-transparent',
        label=_("Card Background Colour")
    )

    class Meta:
        icon = "fa-quote-left"
        template = "blocks/blockquote.html"

class Link_Value(wagtail_blocks.StructValue):
    """ Additional logic for the Link class """

    def url(self) -> str:
        internal_page = self.get("internal_page")
        url_link = self.get("url_link")
        if internal_page:
            return internal_page.localized.url
        elif url_link:
            if url_link.startswith('/'): # presumes internal link starts with '/' and no lang code
                url = '/' + Locale.get_active().language_code + url_link
            else: # external link, do not translate but add new tab instruction
                #@TODO: target blank doesn't work on buttons, look for a workaround
                url = url_link + '" target="_blank' 
            return url
        else:
            return None

class Link(wagtail_blocks.StructBlock):
    button_text = wagtail_blocks.CharBlock(
        max_length=50,
        null=False,
        blank=False,
        label=_("Button Text")
    )
    internal_page = wagtail_blocks.PageChooserBlock(
        required=False,
        label=_("Link to internal page")
    )
    url_link = wagtail_blocks.CharBlock(
        required=False,
        label=_("Link to external site or internal URL")
    )
    appearance = ButtonChoiceBlock(
        max_length=15,
        default='btn-primary',
        label=_("Button Appearance")
    )
    placement = wagtail_blocks.ChoiceBlock(
        max_length=15,
        default='right',
        choices=[
            ('left', _("Left")),
            ('center', _("Centre")),
            ('right', _("Right")),
        ],
        label=_("Button Placement")
    )
    size = wagtail_blocks.ChoiceBlock(
        max_length=10,
        default=' ',
        choices=[
            ('btn-sm', _("Small")),
            (' ', _("Standard")),
            ('btn-lg', _("Large")),
        ],
        label=_("Button Size")
    )
    class Meta:
        value_class = Link_Value
        icon = "fa-link"
        template = "blocks/link_button.html"

    def clean(self, value):
        errors = {}
        internal_page = value.get('internal_page')
        url_link = value.get('url_link')

        if not(bool(internal_page) ^ bool(url_link)):
            errors['internal_page'] = ErrorList(["Please select an internal page or an external link (but not both)"])
            errors['url_link'] = ErrorList(["Please select an internal page or an external link (but not both)"])

        if errors:
            raise ValidationError("Please check the errors below and correct before saving", params=errors)

        return super().clean(value)

class SimpleRichTextBlock(wagtail_blocks.StructBlock):
    content = wagtail_blocks.RichTextBlock(
                features= [
                    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                    'bold',
                    'italic',
                    'ol',
                    'ul',
                    'link',
                    'hr',
                    'center',
                    'right',
                ]
    )

    class Meta:
        template = 'blocks/simple_richtext_block.html'
        label = _("Formatted Text Block")
        icon = 'fa-text-height'

class FlexCard(wagtail_blocks.StructBlock):
    
    format = wagtail_blocks.ChoiceBlock(
        max_length=15,
        default='vertical',
        choices=[
            ('image-left-responsive', _("Responsive Horizontal (Image left of text on widescreen only)")),
            ('image-right-responsive', _("Responsive Horizontal (Image right of text on widescreen only)")),
            ('image-left-fixed', _("Fixed Horizontal (Image left of text on all screen sizes)")),
            ('image-right-fixed', _("Fixed Horizontal (Image right of text on all screen sizes)")),
            ('vertical', _("Vertical (Image above text on on all screen sizes)")),
        ],
        label=_("Card Format")
    )    
    background = ColourThemeChoiceBlock(
        default='bg-transparent',
        label=_("Card Background Colour")
    )
    border = wagtail_blocks.BooleanBlock(
        default=True,
        required=False,
        label=_("Border"),
        help_text=_("Draw a border around the card?")
    )
    text = SimpleRichTextBlock(
        label=_("Card Body Text"),
        help_text=_("Body text for this card."),
    )
    image = SEOImageChooseBlock(
        label=_("Select Image & Enter Details"),
        help_text=_("Card Image (approx 1:1.4 ratio - ideally upload 2100x1470px)."),
    )

    class Meta:
        template = 'blocks/flex_card_block.html'
        label = _("Image & Text Card")
        icon = 'fa-address-card'

class CallToActionCard(FlexCard):
    link = Link(
        label=_("Link Button"),
        help_text = _("Enter a link or select a page and choose button options."),
        required=False,
    )
    class Meta:
        template = 'blocks/flex_card_block.html'
        label = _("Call-To-Action Card (Image/Text/Button)")
        icon = 'fa-address-card'

class SimpleCard(wagtail_blocks.StructBlock):
    background = ColourThemeChoiceBlock(
        default='bg-transparent',
        label=_("Card Background Colour")
    )    
    border = wagtail_blocks.BooleanBlock(
        default=True,
        required=False,
        label=_("Border"),
        help_text=_("Draw a border around the card?")
    )
    text = SimpleRichTextBlock(
        label=_("Card Body Text"),
        help_text=_("Body text for this card."),
    )

    class Meta:
        template = 'blocks/simple_card_block.html'
        label = _("Simple Card (Text Only)")
        icon = 'fa-align-justify'

class SimpleCardStreamBlock(StreamBlock):
    simple_card = SimpleCard()

class SimpleCardGridBlock(wagtail_blocks.StructBlock):
    columns = wagtail_blocks.ChoiceBlock(
        max_length=40,
        default='row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4',
        choices=[
            ('row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4', _("Mobile:1 Max:4")),
            ('row-cols-1 row-cols-md-2', _("Mobile:1 Max:2")),
            ('row-cols-2 row-cols-md-3 row-cols-lg-4', _("Mobile:2 Max:4")),
        ],
        label=_("Maximum Cards per Row")
    )
    cards = SimpleCardStreamBlock()

    class Meta:
        template = "blocks/simple_card_grid_block.html"
        icon = 'fa-th'
        label = _("Flexible Grid of Simple Cards")

class InlineVideoBlock(wagtail_blocks.StructBlock):
    video = EmbedBlock(
        label=_("Video URL"),
        help_text = _("eg 'https://www.youtube.com/watch?v=kqN1HUMr22I'")
    )
    caption = CharBlock(required=False, label=_("Caption"))
    float = wagtail_blocks.ChoiceBlock(
        required=False,
        choices=[('right', _("Right")), ('left', _("Left")), ('center', _("Center"))],
        default='right',
        label=_("Float"),
    )
    size = wagtail_blocks.ChoiceBlock(
        required=False,
        choices=[('small', _("Small")), ('medium', _("Medium")), ('large', _("Large"))],
        default='small',
        label=_("Size"),
    )

    class Meta:
        icon = 'media'
        template = 'blocks/inline_video_block.html'
        label = _("Embed external video")    

class SocialMediaEmbedBlock(wagtail_blocks.StructBlock):
    embed_code = RawHTMLBlock(
        label=_("Paste Embed code block from Provider"),
        help_text=_("Paste in only embed code. For Facebook, only Step 2 on the JavaScript SDK tab")
    )
    class Meta:
        template='blocks/social_media_embed.html',
        icon = 'fa-share-alt-square'
        label = _("Embed Social Media Post")

class HiddenField(Input):
    input_type = 'hidden'
    template_name = 'django/forms/widgets/hidden.html'

class HiddenCharBlock(CharBlock):

    #TODO: 
    # trying to make a hidden field in the block
    # this needs fixing - either turn it into a readonly panel or find out where
    # the label comes from and disable it there (probably in the struct block)

    def field(self):
        field_kwargs = {'widget': HiddenField()}
        field_kwargs.update(self.field_options)
        return forms.CharField(**field_kwargs)
    def render_form(self, value, prefix='', errors=None):
        field = self.field
        widget = HiddenField()

        widget_attrs = {'id': prefix, 'placeholder': self.label, 'input_type': 'hidden'}

        field_value = field.prepare_value(self.value_for_form(value))

        if hasattr(widget, 'render_with_errors'):
            widget_html = widget.render_with_errors(prefix, field_value, attrs=widget_attrs, errors=errors)
            widget_has_rendered_errors = True
        else:
            widget_html = widget.render(prefix, field_value, attrs=widget_attrs)
            widget_has_rendered_errors = False

        return render_to_string('blocks/hidden_field.html', {
            'name': self.name,
            'classes': getattr(self.meta, 'form_classname', self.meta.classname),
            'widget': widget_html,
            'field': field,
            'errors': errors if (not widget_has_rendered_errors) else None
        })
    def clean(self, value):
        return None
    @property
    def required(self):
        # a FieldBlock is required if and only if its underlying form field is required
        return False

class ExternalLinkEmbedBlock(wagtail_blocks.StructBlock):
    external_link = URLBlock(
        label=_("URL to External Article"),
        help_text=_("For articles in external websites without embed share option"),
    )
    link_text = wagtail_blocks.CharBlock(
        label=_("Text for link to article"),
        default=_("Read Full Article")
    )

    class Meta:
        template='blocks/external_link_embed.html',
        icon = 'fa-share-alt'
        label = _("Embed External Article")
    
class CarouselImageBlock(wagtail_blocks.StructBlock):
    image = SEOImageChooseBlock(label=_("Select Image & Enter Details"))
    title = wagtail_blocks.CharBlock(label=_("Optional Image Title"), required=False)
    caption = wagtail_blocks.TextBlock(label=_("Optional Image Caption"), required=False)
    link = wagtail_blocks.PageChooserBlock(
        required=False,
        label=_("Optional Link to Internal Page")
    )
    class Meta:
        icon = 'image'
        label = _("Image for Carousel")

class CarouselImageStreamBlock(StreamBlock):
    carousel_image = CarouselImageBlock()

class ImageCarouselBlock(wagtail_blocks.StructBlock):
    format = ImageFormatChoiceBlock(
        default='4-3',
        label=_("Select image aspect ratio"),
    )
    heading = wagtail_blocks.CharBlock(
        label=_("Carousel Title"), 
        required=False,
    )
    carousel_images = CarouselImageStreamBlock(min_num=2, max_num=5)
    
    class Meta:
        template='blocks/image_carousel.html'
        icon="fa-clone"
        label = _("Image Carousel")

class CollapsableCard(wagtail_blocks.StructBlock):
    header = wagtail_blocks.CharBlock(
        label=_("Card Banner Title")
    )
    text = SimpleRichTextBlock(
        label=_("Card Body Text"),
        help_text=_("Body text for this card."),
    )

class CollapsableCardStreamBlock(StreamBlock):
    collapsable_card = CollapsableCard()

class CollapsableCardBlock(wagtail_blocks.StructBlock):
    header_colour  = ColourThemeChoiceBlock(
        default='text-white bg-dark',
        label=_("Card Header Background Colour")
    )    
    body_colour  = ColourThemeChoiceBlock(
        default='text-black bg-light',
        label=_("Card Body Background Colour")
    )
    cards = CollapsableCardStreamBlock(min_num=2)

    class Meta:
        template='blocks/collapsable_card_block.html'
        icon="fa-stack-overflow"
        label = _("Collapsable Text Block")

class EmptyStaticBlock(wagtail_blocks.StaticBlock):
    class Meta:
        template = 'blocks/empty_block.html'
        icon = 'placeholder'
        label = 'Empty Block'

class SpacerStaticBlock(wagtail_blocks.StaticBlock):
    class Meta:
        template = 'blocks/spacer_block.html'
        icon = 'fa-square'
        label = 'Add Blank Space'

class RandomTestimonialBlock(wagtail_blocks.StaticBlock):
    class Meta:
        template = 'blocks/random_testimonial_block.html'
        icon = 'fa-comment'
        label = 'Random Testimonial'

class LatestBlogPostGrid(StructBlock):
    group_label = SimpleRichTextBlock(
        blank=True,
        null=True,
        label=_("Optional heading for block"),
        help_text=_("Leave blank for no heading"),
        required=False
    )
    background = ColourThemeChoiceBlock(
        default='bg-transparent',
        label=_("Card Background Colour")
    )
    post_count = IntegerBlock(
        default=2,
        min_value=1,
        max_value=20,
        label=_("Number of blog posts to show")
    )
    class Meta:
        template = 'blocks/latest_blog_posts_block.html'
        label = _("Latest Blog Post(s)")
        icon = 'fa-edit'


class BaseStreamBlock(StreamBlock):
    # header_block = HeaderBlock()
    richtext_block = SimpleRichTextBlock()
    image_block = ImageBlock()
    block_quote = BlockQuote()
    link_button = Link()
    flex_card = FlexCard()
    call_to_action_card = CallToActionCard()
    simple_card = SimpleCard()
    simple_card_grid = SimpleCardGridBlock()
    collapsible_card_block = CollapsableCardBlock()
    social_media_embed = SocialMediaEmbedBlock()
    external_link_embed = ExternalLinkEmbedBlock()
    inline_video_block = InlineVideoBlock()
    image_carousel = ImageCarouselBlock()
    latest_blog_posts = LatestBlogPostGrid()
    random_testimonial = RandomTestimonialBlock()
    spacer_block = SpacerStaticBlock()
    empty_block = EmptyStaticBlock()

class TwoColumnLayoutChoiceBlock(wagtail_blocks.ChoiceBlock):
    choices = [
        ('auto-', _("Left column width determined by content (care needed, test on all screen sizes)")),
        ('-auto', _("Right column width determined by content (care needed, test on all screen sizes)")),
        ('1-11', _("Left 1, Right 11")),
        ('2-10', _("Left 2, Right 10")),
        ('3-9', _("Left 3, Right 9")),
        ('4-8', _("Left 4, Right 8")),
        ('5-7', _("Left 5, Right 7")),
        ('6-6', _("Left 6, Right 6")),
        ('7-5', _("Left 7, Right 5")),
        ('8-4', _("Left 8, Right 4")),
        ('9-3', _("Left 9, Right 3")),
        ('10-2', _("Left 10, Right 2")),
        ('11-1', _("Left 11, Right 1")),
    ]

class ThreeColumnLayoutChoiceBlock(wagtail_blocks.ChoiceBlock):
    choices = [
        ('-auto-', _("Centre column width determined by content (care needed, test on all screen sizes)")),
        ('4-4-4', _("Equal Width Columns")),
        ('3-6-3', _("Left 3, Centre 6, Right 3")),
        ('2-8-2', _("Left 2, Centre 8, Right 2")),
        ('1-10-1', _("Left 1, Centre 10, Right 1")),
    ]

class BreakPointChoiceBlock(wagtail_blocks.ChoiceBlock):
    choices = [
        ('-', _("Columns side by side on all screen sizes (best for uneven column sizes)")),
        ('-md', _("Columns side by side on medium and large screen only")),
        ('-sm', _("Single column on mobile, side by side on all other screens"))
    ]

class FullWidthBaseBlock(wagtail_blocks.StructBlock):
    column = BaseStreamBlock(
        label=_("Single Column Contents"),
        blank=True,
        Null=True
    )

    class Meta:
        template = 'blocks/full_width_block.html'
        icon = 'arrows-alt-h'
        label = "Page Wide Block"

class TwoColumnBaseBlock(wagtail_blocks.StructBlock):
    column_layout = TwoColumnLayoutChoiceBlock(
        default = '6-6',
        label = _("Select column size ratio")
    )
    breakpoint = BreakPointChoiceBlock(
        default = '-sm',
        label = _("Select responsive layout behaviour")
    )
    left_column = BaseStreamBlock(
        label=_("Left Column Contents"),
        blank=True,
        Null=True
    )
    right_column = BaseStreamBlock(
        label=_("Right Column Contents"),
        blank=True,
        Null=True
    )

    class Meta:
        template = 'blocks/two_column_block.html'
        icon = 'fa-columns'
        label = "Two Column Block"

class ThreeColumnBaseBlock(wagtail_blocks.StructBlock):
    column_layout = ThreeColumnLayoutChoiceBlock(
        default = '4-4-4',
        label = _("Select column size ratio")
    )
    breakpoint = BreakPointChoiceBlock(
        default = '-md',
        label = _("Select responsive layout behaviour")
    )
    left_column = BaseStreamBlock(
        label=_("Left Column Contents"),
        blank=True,
        Null=True
    )
    centre_column = BaseStreamBlock(
        label=_("Centre Column Contents"),
        blank=True,
        Null=True
    )
    right_column = BaseStreamBlock(
        label=_("Right Column Contents"),
        blank=True,
        Null=True
    )

    class Meta:
        template = 'blocks/three_column_block.html'
        icon = 'fa-columns'
        label = "Three Column Block"

class GridStreamBlock(StreamBlock):
    page_wide_block=FullWidthBaseBlock()
    two_column_block = TwoColumnBaseBlock()
    three_column_block = ThreeColumnBaseBlock()
