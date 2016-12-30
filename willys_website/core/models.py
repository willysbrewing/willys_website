from __future__ import unicode_literals

from django import forms
from django.core.mail import EmailMessage
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.shortcuts import render
from django.utils.functional import cached_property
from django.core.validators import RegexValidator

from modelcluster.fields import ParentalKey
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.wagtailadmin.edit_handlers import (FieldPanel, InlinePanel,
                                                MultiFieldPanel,
                                                PageChooserPanel,
                                                StreamFieldPanel)
from wagtail.wagtailadmin.utils import send_mail
from wagtail.wagtailcore.blocks import (CharBlock, FieldBlock, ListBlock,
                                        PageChooserBlock, RawHTMLBlock,
                                        RichTextBlock, StreamBlock,
                                        StructBlock, TextBlock)
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailcore.models import Orderable, Page
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailforms.models import AbstractEmailForm, AbstractFormField
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.models import (AbstractImage, AbstractRendition,
                                          Image)
from wagtail.wagtailsearch import index
from wagtail.wagtailsnippets.models import register_snippet

# Streamfield blocks and config
class LinkFields(models.Model):
    link_external = models.URLField("External link", blank=True)
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        related_name='+'
    )

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        else:
            return self.link_external

    panels = [
        PageChooserPanel('link_page'),
        FieldPanel('link_external'),
    ]

    class Meta:
        abstract = True

# Home Page
class HomePageHero(Orderable, LinkFields):
    page = ParentalKey('willys_website.HomePage', related_name='hero')
    background = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    color = models.CharField(
        max_length=7,
        null=True,
        blank=True,
        validators=[RegexValidator(regex='^#(?:[0-9a-fA-F]{3}){1,2}$')],
        help_text="Background Color Hex #ffffff")
    name = models.CharField(max_length=255)
    claim = models.CharField(max_length=255)
    position = models.CharField(max_length=1, default=('R', 'Right'), choices=(('L', 'Left'), ('R', 'Right')))

    panels = [
        FieldPanel('name'),
        FieldPanel('claim'),
        FieldPanel('position'),
        ImageChooserPanel('background'),
        FieldPanel('color'),
    ] + LinkFields.panels


class HomePage(Page):
    class Meta:
        verbose_name = "Homepage"

    content_panels = [
        FieldPanel('title', classname="full title"),
        InlinePanel('hero', label="Hero"),
    ]


# Standard page

class StandardPage(Page):
    main_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    heading = models.CharField(max_length=255)
    streamfield = StreamField([
        ('heading', CharBlock(classname="full title")),
        ('paragraph', RichTextBlock()),
        ('image', ImageChooserBlock()),
    ])

    content_panels = [
        FieldPanel('title', classname="full title"),
        ImageChooserPanel('main_image'),
        FieldPanel('heading'),
        StreamFieldPanel('streamfield'),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
    ]
