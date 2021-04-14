# Generated by Django 3.1.8 on 2021-04-13 16:04

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.embeds.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_auto_20210413_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='body',
            field=wagtail.core.fields.StreamField([('header_block', wagtail.core.blocks.StructBlock([('header', wagtail.core.blocks.ChoiceBlock(choices=[('h1', 'H1'), ('h2', 'H2'), ('h3', 'H3'), ('h4', 'H4'), ('h5', 'H5'), ('h6', 'H6')], label='Header Size')), ('text', wagtail.core.blocks.CharBlock(label='Text', max_length=50))])), ('list_block', wagtail.core.blocks.StructBlock([('content', wagtail.core.blocks.ListBlock(wagtail.core.blocks.CharBlock(), label='Items'))])), ('image_text_overlay', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(label='Image')), ('text', wagtail.core.blocks.CharBlock(label='Text', max_length=200))])), ('cropped_images_with_text', wagtail.core.blocks.StructBlock([('image_items', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(label='Image')), ('text', wagtail.core.blocks.CharBlock(label='Text', max_length=200))]), label='Image Item'))])), ('list_with_images', wagtail.core.blocks.StructBlock([('list_items', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(label='Image')), ('title', wagtail.core.blocks.CharBlock(label='Title', max_length=200)), ('text', wagtail.core.blocks.CharBlock(label='Text', max_length=200)), ('link_text', wagtail.core.blocks.CharBlock(label='Link Text', max_length=200, required=False)), ('link_url', wagtail.core.blocks.URLBlock(label='Link URL', max_length=200, required=False))]), label='List Item'))])), ('thumbnail_gallery', wagtail.core.blocks.StructBlock([('image_items', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(label='Image'))]), label='Image'))])), ('image_slider', wagtail.core.blocks.StructBlock([('image_items', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(label='Image'))]), label='Image'))])), ('paragraph_block', wagtail.core.blocks.RichTextBlock(icon='fa-paragraph', template='blocks/paragraph_block.html')), ('image_block', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('caption', wagtail.core.blocks.CharBlock(required=False)), ('attribution', wagtail.core.blocks.CharBlock(required=False))])), ('block_quote', wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.TextBlock()), ('attribute_name', wagtail.core.blocks.CharBlock(blank=True, label='e.g. Mary Berry', required=False))])), ('embed_block', wagtail.embeds.blocks.EmbedBlock(help_text='Insert an embed URL e.g https://www.youtube.com/embed/SGJFWirQ3ks', icon='fa-s15', template='blocks/embed_block.html')), ('link_block', wagtail.core.blocks.StructBlock([('link_text', wagtail.core.blocks.CharBlock(default='More Details', max_length=50)), ('internal_page', wagtail.core.blocks.PageChooserBlock(required=False)), ('external_link', wagtail.core.blocks.URLBlock(required=False))])), ('card_block', wagtail.core.blocks.StructBlock([('cards', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(help_text='Title text for the card (maximum 100 characters).', max_length=100)), ('text', wagtail.core.blocks.TextBlock(help_text='Optional body text for this card (maximum 255 characters).', max_length=255, required=False)), ('image', wagtail.images.blocks.ImageChooserBlock(help_text='Card Image (cropped to 570x370px).')), ('link', wagtail.core.blocks.StructBlock([('link_text', wagtail.core.blocks.CharBlock(default='More Details', max_length=50)), ('internal_page', wagtail.core.blocks.PageChooserBlock(required=False)), ('external_link', wagtail.core.blocks.URLBlock(required=False))], help_text='Enter a link or select a page.'))])))])), ('image_and_text_block', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(help_text='Image cropped to 786x552px')), ('image_alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left Aligned Image'), ('right', 'Right Aligned Image')], help_text='Select Image Placement')), ('title', wagtail.core.blocks.CharBlock(help_text='Max length 60 characters', max_length=60)), ('text', wagtail.core.blocks.CharBlock(help_text='Optional text - max length 140 characters', max_length=140, required=False)), ('link', wagtail.core.blocks.StructBlock([('link_text', wagtail.core.blocks.CharBlock(default='More Details', max_length=50)), ('internal_page', wagtail.core.blocks.PageChooserBlock(required=False)), ('external_link', wagtail.core.blocks.URLBlock(required=False))]))])), ('call_to_action_block', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(help_text='Max length 200 characters', max_length=200)), ('link', wagtail.core.blocks.StructBlock([('link_text', wagtail.core.blocks.CharBlock(default='More Details', max_length=50)), ('internal_page', wagtail.core.blocks.PageChooserBlock(required=False)), ('external_link', wagtail.core.blocks.URLBlock(required=False))]))])), ('inline_image_block', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(label='Image')), ('caption', wagtail.core.blocks.CharBlock(label='Caption', required=False)), ('float', wagtail.core.blocks.ChoiceBlock(choices=[('right', 'Right'), ('left', 'Left'), ('center', 'Center')], label='Float', required=False)), ('size', wagtail.core.blocks.ChoiceBlock(choices=[('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], label='Size', required=False))])), ('inline_video_block', wagtail.core.blocks.StructBlock([('video', wagtail.embeds.blocks.EmbedBlock(label='Video')), ('caption', wagtail.core.blocks.CharBlock(label='Caption', required=False)), ('float', wagtail.core.blocks.ChoiceBlock(choices=[('right', 'Right'), ('left', 'Left'), ('center', 'Center')], label='Float', required=False)), ('size', wagtail.core.blocks.ChoiceBlock(choices=[('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], label='Size', required=False))]))], blank=True, verbose_name='Page body'),
        ),
    ]
