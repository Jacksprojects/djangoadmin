# Generated by Django 3.2.7 on 2021-12-01 16:35

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0003_taggeditem_add_unique_index'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Titre')),
                ('slug', models.SlugField(unique=True, verbose_name='Slug')),
                ('extract', models.TextField(blank=True, max_length=300, null=True, verbose_name='Extrait')),
                ('content', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Contenu')),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date de publication')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Dernière modification')),
                ('status', models.CharField(choices=[('DR', 'Draft'), ('PB', 'Published')], default='DR', max_length=10, verbose_name='Statut du poste')),
                ('author', models.ForeignKey(blank=True, editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'Blog Post',
                'verbose_name_plural': 'Blog Posts',
                'ordering': ('-date_posted',),
            },
        ),
    ]
