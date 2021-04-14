# Generated by Django 3.1.8 on 2021-04-13 14:34

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0023_add_choose_permissions'),
        ('wagtailcore', '0060_fix_workflow_unique_constraint'),
        ('home', '0005_testimonial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='testimonial',
            old_name='attribution',
            new_name='author',
        ),
        migrations.AddField(
            model_name='testimonial',
            name='author_link',
            field=models.URLField(blank=True, help_text='Optional link to testimonial author', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='testimonial',
            name='locale',
            field=models.ForeignKey(default='1', editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='wagtailcore.locale'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='testimonial',
            name='photo',
            field=models.ForeignKey(help_text='Photo of image 25x25', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
        migrations.AddField(
            model_name='testimonial',
            name='reference_text',
            field=models.TextField(default='fffffffffff', help_text='Reference text', max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='testimonial',
            name='translation_key',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AlterUniqueTogether(
            name='testimonial',
            unique_together={('translation_key', 'locale')},
        ),
        migrations.RemoveField(
            model_name='testimonial',
            name='quote',
        ),
    ]
