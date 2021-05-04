# Generated by Django 3.1.8 on 2021-05-02 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0014_auto_20210502_1039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactpage',
            name='subject',
            field=models.CharField(help_text='Subject Line for Notification Email. Will be suffuxed by Date/Time.', max_length=255, verbose_name='subject'),
        ),
    ]
