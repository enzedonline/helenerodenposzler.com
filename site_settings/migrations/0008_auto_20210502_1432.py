# Generated by Django 3.1.8 on 2021-05-02 12:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('site_settings', '0007_emailsignature'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='emailsignature',
            options={'verbose_name': 'Email Signature', 'verbose_name_plural': 'Email Signatures'},
        ),
    ]
