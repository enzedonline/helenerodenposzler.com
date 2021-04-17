from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.core.blocks import (
    CharBlock, ChoiceBlock, RichTextBlock, StreamBlock, StructBlock, TextBlock,
)
from wagtail_blocks.blocks import *
from wagtail_localize.synctree import Locale

class ImageBlock(StructBlock):
    """
    Custom `StructBlock` for utilizing images with associated caption and
    attribution data
    """
    image = ImageChooserBlock(required=True)
    caption = CharBlock(required=False)
    attribution = CharBlock(required=False)

    class Meta:
        icon = 'image'
        template = "blocks/image_block.html"

class BlockQuote(StructBlock):
    """
    Custom `StructBlock` that allows the user to attribute a quote to the author
    """
    text = TextBlock()
    attribute_name = CharBlock(
        blank=True, required=False, label='Optional Attribution')

    class Meta:
        icon = "fa-quote-left"
        template = "blocks/blockquote.html"

class Link_Value(blocks.StructValue):
    """ Additional logic for the Link class """

    def url(self) -> str:
        internal_page = self.get("internal_page")
        external_link = self.get("external_link")
        if internal_page:
            return internal_page.localized.url
        elif external_link:
            if external_link.startswith('/'): # presumes internal link starts with '/' and no lang code
                url = '/' + Locale.get_active().language_code + external_link
            else: # external link, do nothing
                url = external_link
            return url
        else:
            return None

class Link(blocks.StructBlock):
    link_text = blocks.CharBlock(
        max_length=50,
        default='More Details',
        label="Button Text"
    )
    internal_page = blocks.PageChooserBlock(
        required=False,
    )
    external_link = blocks.CharBlock(
        required=False,
    )

    class Meta:
        value_class = Link_Value
        icon = "fa-link"
        template = "blocks/link_button.html"

    def clean(self, value):
        errors = {}
        internal_page = value.get('internal_page')
        external_link = value.get('external_link')

        if not(bool(internal_page) ^ bool(external_link)):
            errors['internal_page'] = ErrorList(["Please select an internal page or an external link (but not both)"])
            errors['external_link'] = ErrorList(["Please select an internal page or an external link (but not both)"])

        if errors:
            raise ValidationError("Please check the errors below and correct before saving", params=errors)

        return super().clean(value)

class SimpleRichTextBlock(blocks.StructBlock):
    content = blocks.RichTextBlock(
                features= [
                    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                    'bold',
                    'italic',
                    'ol',
                    'ul',
                    'link',
                    'hr ',
                ]
    )

    class Meta:
        template = 'blocks/simple_richtext_block.html'
        label = _("Formatted Text Block")
        icon = 'fa-text-height'

class Card(blocks.StructBlock):
    title = blocks.CharBlock(
        max_length=100,
        help_text='Title text for the card (maximum 100 characters).',
    )
    text = blocks.TextBlock(
        max_length=255,
        help_text='Optional body text for this card (maximum 255 characters).',
        required=False,
    )
    image = ImageChooserBlock(
        help_text='Card Image (cropped to 570x370px).',
    )
    link = Link(
        help_text = 'Enter a link or select a page.'
    )

class CardsBlock(blocks.StructBlock):

    cards = blocks.ListBlock(
        Card()
    )

    class Meta:
        template = "blocks/card_block.html"
        icon = "image"
        label = "Standard Cards"

class RadioSelectBlock(blocks.ChoiceBlock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.field.widget = forms.RadioSelect(
            choices = self.field.widget.choices
        )

class ImageAndTextBlock(blocks.StructBlock):
    image = ImageChooserBlock(
        help_text='Image cropped to 786x552px'
    )
    image_alignment = RadioSelectBlock(
        choices=(
            ('left', "Left Aligned Image"),
            ('right', "Right Aligned Image"),
        ),
        default='left',
        help_text='Select Image Placement',
    )
    title = blocks.CharBlock(
        max_length=60,
        help_text='Max length 60 characters',
    )
    text = blocks.CharBlock(
        max_length=140,
        required=False,
        help_text='Optional text - max length 140 characters'
    )
    link=Link()

    class Meta:
        template = 'blocks/image_and_text_block.html'
        icon = 'image'
        label = "Image & Text"

class CallToActionBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        max_length=200,
        help_text="Max length 200 characters"
    )
    link = Link()

    class Meta:
        template = 'blocks/call_to_action_block.html'
        icon = 'plus'
        label = "Call to Action"

class InlineImageBlock(blocks.StructBlock):
    image = ImageChooserBlock(label=_("Image"))
    caption = CharBlock(required=False, label=_("Caption"))
    float = blocks.ChoiceBlock(
        required=False,
        choices=[('right', _("Right")), ('left', _("Left")), ('center', _("Center"))],
        default='right',
        label=_("Float"),
    )
    size = blocks.ChoiceBlock(
        required=False,
        choices=[('small', _("Small")), ('medium', _("Medium")), ('large', _("Large"))],
        default='small',
        label=_("Size"),
    )

    class Meta:
        icon = 'image'

class InlineVideoBlock(blocks.StructBlock):
    video = EmbedBlock(label=_("Video"))
    caption = CharBlock(required=False, label=_("Caption"))
    float = blocks.ChoiceBlock(
        required=False,
        choices=[('right', _("Right")), ('left', _("Left")), ('center', _("Center"))],
        default='right',
        label=_("Float"),
    )
    size = blocks.ChoiceBlock(
        required=False,
        choices=[('small', _("Small")), ('medium', _("Medium")), ('large', _("Large"))],
        default='small',
        label=_("Size"),
    )

    class Meta:
        icon = 'media'
    


# StreamBlocks
class BaseStreamBlock(StreamBlock):
    """
    Define the custom blocks that `StreamField` will utilize
    """

    # header_block = HeaderBlock()
    # list_block = ListBlock()
    # image_text_overlay = ImageTextOverlayBlock()
    # cropped_images_with_text = CroppedImagesWithTextBlock()
    # list_with_images = ListWithImagesBlock()
    # thumbnail_gallery = ThumbnailGalleryBlock()
    # image_slider = ImageSliderBlock()
    # paragraph_block = RichTextBlock(
    #     icon="fa-paragraph",
    #     template="blocks/paragraph_block.html"
    # )
    richtext_block = SimpleRichTextBlock()
    image_block = ImageBlock()
    block_quote = BlockQuote()
    # embed_block = EmbedBlock(
    #     help_text='Insert an embed URL e.g https://www.youtube.com/embed/SGJFWirQ3ks',
    #     icon="fa-s15",
    #     template="blocks/embed_block.html")
    link_button = Link()
    # card_block = CardsBlock()
    # image_and_text_block = ImageAndTextBlock()
    # call_to_action_block = CallToActionBlock()
    # inline_image_block = InlineImageBlock()
    # inline_video_block = InlineVideoBlock()