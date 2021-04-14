# Generated by Django 3.1.7 on 2021-03-18 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0023_auto_20210318_1350'),
    ]

    operations = [
        migrations.AddField(
            model_name='autofillmenuitem',
            name='only_show_in_menus',
            field=models.BooleanField(default=False, help_text="If selected, only pages with 'Show In Menu' selected will be shown.", verbose_name="Include only 'Show In Menu' pages"),
        ),
    ]
