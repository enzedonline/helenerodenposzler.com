# Generated by Django 3.1.8 on 2021-05-03 19:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_bloglistingpage_read_more_button_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bloglistingpage',
            name='read_more_button_text',
        ),
    ]
