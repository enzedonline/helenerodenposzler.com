# Generated by Django 3.1.8 on 2021-04-30 20:02

from django.db import migrations, models
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0006_contactpage_formfield'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactpage',
            name='submit_button_text',
            field=models.CharField(default='Submit', max_length=20, verbose_name='Submit Button Text'),
        ),
        migrations.AlterField(
            model_name='contactpage',
            name='intro',
            field=wagtail.core.fields.RichTextField(blank=True, verbose_name='Introduction Text'),
        ),
        migrations.AlterField(
            model_name='contactpage',
            name='thank_you_text',
            field=wagtail.core.fields.RichTextField(blank=True, verbose_name='Acknowledgement Text to Display After Submit'),
        ),
    ]
