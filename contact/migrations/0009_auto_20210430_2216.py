# Generated by Django 3.1.8 on 2021-04-30 20:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0023_add_choose_permissions'),
        ('contact', '0008_contactpage_intro_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactpage',
            name='intro_image',
            field=models.ForeignKey(blank=True, help_text='Image to display in left column on widescreen only', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image', verbose_name='Introduction Image (optional)'),
        ),
    ]
