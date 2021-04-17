# Generated by Django 3.1.8 on 2021-04-15 19:08

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0020_auto_20210415_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='body',
            field=wagtail.core.fields.StreamField([('image_block', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('caption', wagtail.core.blocks.CharBlock(required=False)), ('attribution', wagtail.core.blocks.CharBlock(required=False))])), ('block_quote', wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.TextBlock()), ('attribute_name', wagtail.core.blocks.CharBlock(blank=True, label='Optional Attribution', required=False))])), ('link_button', wagtail.core.blocks.StructBlock([('link_text', wagtail.core.blocks.CharBlock(default='More Details', label='Button Text', max_length=50)), ('internal_page', wagtail.core.blocks.PageChooserBlock(required=False)), ('external_link', wagtail.core.blocks.CharBlock(required=False))]))], blank=True, verbose_name='Page body'),
        ),
    ]
