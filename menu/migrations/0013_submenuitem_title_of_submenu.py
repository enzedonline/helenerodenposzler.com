# Generated by Django 3.1.7 on 2021-03-08 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0012_auto_20210308_1734'),
    ]

    operations = [
        migrations.AddField(
            model_name='submenuitem',
            name='title_of_submenu',
            field=models.CharField(help_text='Enter the menu-ID that this sub-menu will load', max_length=50, null=True),
        ),
    ]
