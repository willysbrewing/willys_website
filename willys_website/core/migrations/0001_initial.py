# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-07 23:58
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import modelcluster.contrib.taggit
import modelcluster.fields
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtaildocs.blocks
import wagtail.wagtailimages.blocks
import willys_website.core.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtaildocs', '0007_merge'),
        ('wagtailimages', '0016_deprecate_rendition_filter_relation'),
        ('taggit', '0002_auto_20150616_2121'),
        ('wagtailcore', '0032_add_bulk_delete_page_permission'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='BlogPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('body', wagtail.wagtailcore.fields.StreamField((('h2', wagtail.wagtailcore.blocks.CharBlock(classname='title', icon='title')), ('h3', wagtail.wagtailcore.blocks.CharBlock(classname='title', icon='title')), ('h4', wagtail.wagtailcore.blocks.CharBlock(classname='title', icon='title')), ('intro', wagtail.wagtailcore.blocks.RichTextBlock(icon='pilcrow')), ('paragraph', wagtail.wagtailcore.blocks.RichTextBlock(icon='pilcrow')), ('aligned_image', wagtail.wagtailcore.blocks.StructBlock((('image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('caption', wagtail.wagtailcore.blocks.RichTextBlock()), ('alignment', willys_website.core.models.ImageFormatChoiceBlock())), icon='image', label='Aligned image')), ('pullquote', wagtail.wagtailcore.blocks.StructBlock((('quote', wagtail.wagtailcore.blocks.TextBlock('quote title')), ('attribution', wagtail.wagtailcore.blocks.CharBlock())))), ('aligned_html', wagtail.wagtailcore.blocks.StructBlock((('html', wagtail.wagtailcore.blocks.RawHTMLBlock()), ('alignment', willys_website.core.models.HTMLAlignmentChoiceBlock())), icon='code', label='Raw HTML')), ('document', wagtail.wagtaildocs.blocks.DocumentChooserBlock(icon='doc-full-inverse'))))),
                ('date', models.DateField(verbose_name='Post date')),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='BlogPageRelatedLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('link_external', models.URLField(blank=True, verbose_name='External link')),
                ('title', models.CharField(help_text='Link title', max_length=255)),
                ('link_document', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtaildocs.Document')),
            ],
            options={
                'abstract': False,
                'ordering': ['sort_order'],
            },
        ),
        migrations.CreateModel(
            name='BlogPageTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_items', to='willys_website.BlogPage')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='willys_website_blogpagetag_items', to='taggit.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EventIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='EventPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('date_from', models.DateField(verbose_name='Start date')),
                ('time_from', models.TimeField(default=None, verbose_name='Start time')),
                ('location', models.CharField(max_length=255)),
                ('body', wagtail.wagtailcore.fields.StreamField((('h2', wagtail.wagtailcore.blocks.CharBlock(classname='title', icon='title')), ('h3', wagtail.wagtailcore.blocks.CharBlock(classname='title', icon='title')), ('h4', wagtail.wagtailcore.blocks.CharBlock(classname='title', icon='title')), ('intro', wagtail.wagtailcore.blocks.RichTextBlock(icon='pilcrow')), ('paragraph', wagtail.wagtailcore.blocks.RichTextBlock(icon='pilcrow')), ('aligned_image', wagtail.wagtailcore.blocks.StructBlock((('image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('caption', wagtail.wagtailcore.blocks.RichTextBlock()), ('alignment', willys_website.core.models.ImageFormatChoiceBlock())), icon='image', label='Aligned image')), ('pullquote', wagtail.wagtailcore.blocks.StructBlock((('quote', wagtail.wagtailcore.blocks.TextBlock('quote title')), ('attribution', wagtail.wagtailcore.blocks.CharBlock())))), ('aligned_html', wagtail.wagtailcore.blocks.StructBlock((('html', wagtail.wagtailcore.blocks.RawHTMLBlock()), ('alignment', willys_website.core.models.HTMLAlignmentChoiceBlock())), icon='code', label='Raw HTML')), ('document', wagtail.wagtaildocs.blocks.DocumentChooserBlock(icon='doc-full-inverse'))))),
                ('cost', models.CharField(max_length=255)),
                ('signup_link', models.URLField(blank=True)),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='EventPageRelatedLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('link_external', models.URLField(blank=True, verbose_name='External link')),
                ('title', models.CharField(help_text='Link title', max_length=255)),
                ('link_document', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtaildocs.Document')),
            ],
            options={
                'abstract': False,
                'ordering': ['sort_order'],
            },
        ),
        migrations.CreateModel(
            name='HeroItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link_external', models.URLField(blank=True, verbose_name='External link')),
                ('title', models.CharField(max_length=255)),
                ('claim', models.CharField(max_length=255)),
                ('position', models.CharField(choices=[('left', 'Left'), ('right', 'Right')], default=('left', 'Left'), max_length=5)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'verbose_name': 'Homepage',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='HomePageFeatured',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('link_external', models.URLField(blank=True, verbose_name='External link')),
                ('text', models.CharField(max_length=255)),
                ('background', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
                ('link_document', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtaildocs.Document')),
            ],
            options={
                'abstract': False,
                'ordering': ['sort_order'],
            },
        ),
        migrations.CreateModel(
            name='HomePagePromo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('link_external', models.URLField(blank=True, verbose_name='External link')),
                ('text', models.CharField(max_length=255)),
                ('color', models.CharField(blank=True, help_text='Background Color Hex #ffffff', max_length=7, null=True, validators=[django.core.validators.RegexValidator(regex='^#(?:[0-9a-fA-F]{3}){1,2}$')])),
                ('link_document', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtaildocs.Document')),
            ],
            options={
                'abstract': False,
                'ordering': ['sort_order'],
            },
        ),
        migrations.CreateModel(
            name='ProductIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='ProductPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('name', models.CharField(default=False, max_length=255)),
                ('color', models.CharField(blank=True, help_text='Background Color Hex #ffffff', max_length=7, null=True, validators=[django.core.validators.RegexValidator(regex='^#(?:[0-9a-fA-F]{3}){1,2}$')])),
                ('cost', models.CharField(max_length=255)),
                ('body', wagtail.wagtailcore.fields.StreamField((('h2', wagtail.wagtailcore.blocks.CharBlock(classname='title', icon='title')), ('h3', wagtail.wagtailcore.blocks.CharBlock(classname='title', icon='title')), ('h4', wagtail.wagtailcore.blocks.CharBlock(classname='title', icon='title')), ('intro', wagtail.wagtailcore.blocks.RichTextBlock(icon='pilcrow')), ('paragraph', wagtail.wagtailcore.blocks.RichTextBlock(icon='pilcrow')), ('aligned_image', wagtail.wagtailcore.blocks.StructBlock((('image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('caption', wagtail.wagtailcore.blocks.RichTextBlock()), ('alignment', willys_website.core.models.ImageFormatChoiceBlock())), icon='image', label='Aligned image')), ('pullquote', wagtail.wagtailcore.blocks.StructBlock((('quote', wagtail.wagtailcore.blocks.TextBlock('quote title')), ('attribution', wagtail.wagtailcore.blocks.CharBlock())))), ('aligned_html', wagtail.wagtailcore.blocks.StructBlock((('html', wagtail.wagtailcore.blocks.RawHTMLBlock()), ('alignment', willys_website.core.models.HTMLAlignmentChoiceBlock())), icon='code', label='Raw HTML')), ('document', wagtail.wagtaildocs.blocks.DocumentChooserBlock(icon='doc-full-inverse'))))),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='ProductPageRelatedLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('link_external', models.URLField(blank=True, verbose_name='External link')),
                ('title', models.CharField(help_text='Link title', max_length=255)),
                ('link_document', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtaildocs.Document')),
                ('link_page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.Page')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_links', to='willys_website.ProductPage')),
            ],
            options={
                'abstract': False,
                'ordering': ['sort_order'],
            },
        ),
        migrations.CreateModel(
            name='BlogIndexPageHero',
            fields=[
                ('heroitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='willys_website.HeroItem')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='hero', to='willys_website.BlogIndexPage')),
            ],
            options={
                'abstract': False,
                'ordering': ['sort_order'],
            },
            bases=('willys_website.heroitem', models.Model),
        ),
        migrations.CreateModel(
            name='EventIndexPageHero',
            fields=[
                ('heroitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='willys_website.HeroItem')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='hero', to='willys_website.EventIndexPage')),
            ],
            options={
                'abstract': False,
                'ordering': ['sort_order'],
            },
            bases=('willys_website.heroitem', models.Model),
        ),
        migrations.CreateModel(
            name='HomePageHero',
            fields=[
                ('heroitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='willys_website.HeroItem')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='hero', to='willys_website.HomePage')),
            ],
            options={
                'abstract': False,
                'ordering': ['sort_order'],
            },
            bases=('willys_website.heroitem', models.Model),
        ),
        migrations.CreateModel(
            name='ProductIndexPageHero',
            fields=[
                ('heroitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='willys_website.HeroItem')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='hero', to='willys_website.ProductIndexPage')),
            ],
            options={
                'abstract': False,
                'ordering': ['sort_order'],
            },
            bases=('willys_website.heroitem', models.Model),
        ),
        migrations.CreateModel(
            name='ProductPageHero',
            fields=[
                ('heroitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='willys_website.HeroItem')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='hero', to='willys_website.ProductPage')),
            ],
            options={
                'abstract': False,
                'ordering': ['sort_order'],
            },
            bases=('willys_website.heroitem', models.Model),
        ),
        migrations.AddField(
            model_name='homepagepromo',
            name='link_page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.Page'),
        ),
        migrations.AddField(
            model_name='homepagepromo',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='promo', to='willys_website.HomePage'),
        ),
        migrations.AddField(
            model_name='homepagefeatured',
            name='link_page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.Page'),
        ),
        migrations.AddField(
            model_name='homepagefeatured',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='featured', to='willys_website.HomePage'),
        ),
        migrations.AddField(
            model_name='heroitem',
            name='background',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
        migrations.AddField(
            model_name='heroitem',
            name='link_document',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtaildocs.Document'),
        ),
        migrations.AddField(
            model_name='heroitem',
            name='link_page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.Page'),
        ),
        migrations.AddField(
            model_name='eventpagerelatedlink',
            name='link_page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.Page'),
        ),
        migrations.AddField(
            model_name='eventpagerelatedlink',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_links', to='willys_website.EventPage'),
        ),
        migrations.AddField(
            model_name='blogpagerelatedlink',
            name='link_page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.Page'),
        ),
        migrations.AddField(
            model_name='blogpagerelatedlink',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_links', to='willys_website.BlogPage'),
        ),
        migrations.AddField(
            model_name='blogpage',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='willys_website.BlogPageTag', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
