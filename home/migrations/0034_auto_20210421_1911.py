# Generated by Django 3.1.8 on 2021-04-21 17:11

import core.blocks
from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0033_auto_20210420_1938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='body',
            field=wagtail.core.fields.StreamField([('richtext_block', wagtail.core.blocks.StructBlock([('content', wagtail.core.blocks.RichTextBlock(features=['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'bold', 'italic', 'ol', 'ul', 'link', 'hr', 'center', 'right']))])), ('image_block', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(label='Image', required=True)), ('caption', wagtail.core.blocks.CharBlock(label='Image Caption (optional)', required=False)), ('attribution', wagtail.core.blocks.CharBlock(label='Image Attribution (optional)', required=False))])), ('block_quote', wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.TextBlock(label='Quote')), ('attribute_name', wagtail.core.blocks.CharBlock(blank=True, label='Optional Attribution', required=False))])), ('link_button', wagtail.core.blocks.StructBlock([('button_text', wagtail.core.blocks.CharBlock(blank=False, label='Button Text', max_length=50, null=False)), ('internal_page', wagtail.core.blocks.PageChooserBlock(label='Link to internal page', required=False)), ('url_link', wagtail.core.blocks.CharBlock(label='Link to external site or internal URL', required=False)), ('appearance', wagtail.core.blocks.ChoiceBlock(choices=[('btn-primary', 'Standard Button'), ('btn-btn-secondary', 'Secondary Button'), ('btn-link', 'Text Only'), ('btn-success', 'Success Button'), ('btn-danger', 'Danger Button'), ('btn-warning', 'Warning Button'), ('btn-info', 'Info Button'), ('btn-light', 'Light Button'), ('btn-dark', 'Dark Button')], label='Button Appearance', max_length=15)), ('placement', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left'), ('center', 'Centre'), ('right', 'Right')], label='Button Placement', max_length=15)), ('size', wagtail.core.blocks.ChoiceBlock(choices=[('btn-sm', 'Small'), (' ', 'Standard'), ('btn-lg', 'Large')], label='Button Size', max_length=10))])), ('flex_card', wagtail.core.blocks.StructBlock([('format', wagtail.core.blocks.ChoiceBlock(choices=[('image-left-responsive', 'Responsive Horizontal (Image left of text on widescreen only)'), ('image-right-responsive', 'Responsive Horizontal (Image right of text on widescreen only)'), ('image-left-fixed', 'Fixed Horizontal (Image left of text on all screen sizes)'), ('image-right-fixed', 'Fixed Horizontal (Image right of text on all screen sizes)'), ('vertical', 'Vertical (Image above text on on all screen sizes)')], label='Card Format', max_length=15)), ('background', wagtail.core.blocks.ChoiceBlock(choices=[('bg-transparent', 'Transparent'), ('text-black bg-light', 'Light'), ('text-white bg-dark', 'Dark')], label='Card Background Colour', max_length=25)), ('border', wagtail.core.blocks.BooleanBlock(default=True, help_text='Draw a border around the card?', label='Border', required=False)), ('text', wagtail.core.blocks.StructBlock([('content', wagtail.core.blocks.RichTextBlock(features=['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'bold', 'italic', 'ol', 'ul', 'link', 'hr', 'center', 'right']))], help_text='Body text for this card.', label='Card Body Text')), ('image', wagtail.images.blocks.ImageChooserBlock(help_text='Card Image (approx 1:1.4 ratio - ideally upload 2100x1470px).', label='Image')), ('link', wagtail.core.blocks.StructBlock([('button_text', wagtail.core.blocks.CharBlock(blank=False, label='Button Text', max_length=50, null=False)), ('internal_page', wagtail.core.blocks.PageChooserBlock(label='Link to internal page', required=False)), ('url_link', wagtail.core.blocks.CharBlock(label='Link to external site or internal URL', required=False)), ('appearance', wagtail.core.blocks.ChoiceBlock(choices=[('btn-primary', 'Standard Button'), ('btn-btn-secondary', 'Secondary Button'), ('btn-link', 'Text Only'), ('btn-success', 'Success Button'), ('btn-danger', 'Danger Button'), ('btn-warning', 'Warning Button'), ('btn-info', 'Info Button'), ('btn-light', 'Light Button'), ('btn-dark', 'Dark Button')], label='Button Appearance', max_length=15)), ('placement', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left'), ('center', 'Centre'), ('right', 'Right')], label='Button Placement', max_length=15)), ('size', wagtail.core.blocks.ChoiceBlock(choices=[('btn-sm', 'Small'), (' ', 'Standard'), ('btn-lg', 'Large')], label='Button Size', max_length=10))], help_text='Enter a link or select a page and choose button options.', label='Link Button', required=False))])), ('empty_block', core.blocks.EmptyStaticBlock())], blank=True, verbose_name='Page body'),
        ),
    ]
