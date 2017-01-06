from datetime import date

from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.utils.encoding import python_2_unicode_compatible
from django import forms
from django.core.validators import RegexValidator

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, FieldRowPanel, MultiFieldPanel, \
    InlinePanel, PageChooserPanel, StreamFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailforms.models import AbstractEmailForm, AbstractFormField
from wagtail.wagtailsearch import index

from wagtail.wagtailcore.blocks import TextBlock, StructBlock, StreamBlock, FieldBlock, CharBlock, RichTextBlock, RawHTMLBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtaildocs.blocks import DocumentChooserBlock

from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from taggit.models import TaggedItemBase

##################################################################
########### Global Streamfield definition ########################
##################################################################

class PullQuoteBlock(StructBlock):
    quote = TextBlock("quote title")
    attribution = CharBlock()

    class Meta:
        icon = "openquote"


class ImageFormatChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=(
        ('left', 'Wrap left'), ('right', 'Wrap right'), ('mid', 'Mid width'), ('full', 'Full width'),
    ))


class HTMLAlignmentChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=(
        ('normal', 'Normal'), ('full', 'Full width'),
    ))


class ImageBlock(StructBlock):
    image = ImageChooserBlock()
    caption = RichTextBlock()
    alignment = ImageFormatChoiceBlock()


class AlignedHTMLBlock(StructBlock):
    html = RawHTMLBlock()
    alignment = HTMLAlignmentChoiceBlock()

    class Meta:
        icon = "code"


class BlogStreamBlock(StreamBlock):
    h2 = CharBlock(icon="title", classname="title")
    h3 = CharBlock(icon="title", classname="title")
    h4 = CharBlock(icon="title", classname="title")
    intro = RichTextBlock(icon="pilcrow")
    paragraph = RichTextBlock(icon="pilcrow")
    aligned_image = ImageBlock(label="Aligned image", icon="image")
    pullquote = PullQuoteBlock()
    aligned_html = AlignedHTMLBlock(icon="code", label='Raw HTML')
    document = DocumentChooserBlock(icon="doc-full-inverse")

##################################################################
########### Abstract classes #####################################
##################################################################

class LinkFields(models.Model):
    link_external = models.URLField("External link", blank=True)
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    link_document = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_document:
            return self.link_document.url
        else:
            return self.link_external

    panels = [
        FieldPanel('link_external'),
        PageChooserPanel('link_page'),
        DocumentChooserPanel('link_document'),
    ]

    class Meta:
        abstract = True


class ContactFields(models.Model):
    telephone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address_1 = models.CharField(max_length=255, blank=True)
    address_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    post_code = models.CharField(max_length=10, blank=True)

    panels = [
        FieldPanel('telephone'),
        FieldPanel('email'),
        FieldPanel('address_1'),
        FieldPanel('address_2'),
        FieldPanel('city'),
        FieldPanel('country'),
        FieldPanel('post_code'),
    ]

    class Meta:
        abstract = True

##################################################################
################# HERO ###########################################
##################################################################

class HeroItem(LinkFields):
    title = models.CharField(max_length=255)
    claim = models.CharField(max_length=255)
    position = models.CharField(max_length=5, default=('left', 'Left'), choices=(('left', 'Left'), ('right', 'Right')))
    background = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        FieldPanel('title'),
        FieldPanel('claim'),
        FieldPanel('position'),
        ImageChooserPanel('background'),
        MultiFieldPanel(LinkFields.panels, 'Link'),
    ]

##################################################################
################# RelatedLink ####################################
##################################################################

class RelatedLink(LinkFields):
    title = models.CharField(max_length=255, help_text="Link title")

    panels = [
        FieldPanel('title'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    class Meta:
        abstract = True

##################################################################
################# HomePage #######################################
##################################################################

class HomePageHero(HeroItem):
    page = ParentalKey('willys_website.HomePage', related_name='hero')

class HomePagePromo(Orderable, LinkFields):
    page = ParentalKey('willys_website.HomePage', related_name='promo')
    text = models.CharField(max_length=255)
    color = models.CharField(
        max_length=7,
        null=True,
        blank=True,
        validators=[RegexValidator(regex='^#(?:[0-9a-fA-F]{3}){1,2}$')],
        help_text="Background Color Hex #ffffff")

    panels = [
        FieldPanel('text'),
        FieldPanel('color'),
        MultiFieldPanel(LinkFields.panels, 'Link'),
    ]

class HomePageFeatured(Orderable, LinkFields):
    page = ParentalKey('willys_website.HomePage', related_name='featured')
    text = models.CharField(max_length=255)
    background = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        FieldPanel('text'),
        ImageChooserPanel('background'),
        MultiFieldPanel(LinkFields.panels, 'Link'),
    ]

class HomePage(Page):

    class Meta:
        verbose_name = "Homepage"

    content_panels = Page.content_panels + [
        InlinePanel('hero', label="Hero"),
        InlinePanel('promo', label="Promo"),
        InlinePanel('featured', label="Featured"),
    ]

    promote_panels = Page.promote_panels

##################################################################
################# Standard Index Page ############################
##################################################################

class StandardIndexPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('willys_website.StandardIndexPage', related_name='related_links')


class StandardIndexPage(Page):
    intro = RichTextField(blank=True)
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        InlinePanel('related_links', label="Related links"),
    ]

    promote_panels = Page.promote_panels + [
        ImageChooserPanel('feed_image'),
    ]

##################################################################
################# Standard Page ##################################
##################################################################

class StandardPageHeroItem(Orderable, HeroItem):
    page = ParentalKey('willys_website.StandardPage', related_name='hero')


class StandardPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('willys_website.StandardPage', related_name='related_links')


class StandardPage(Page):
    intro = RichTextField(blank=True)
    body = RichTextField(blank=True)
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        InlinePanel('hero', label="Hero"),
        FieldPanel('body', classname="full"),
        InlinePanel('related_links', label="Related links"),
    ]

    promote_panels = Page.promote_panels + [
        ImageChooserPanel('feed_image'),
    ]

##################################################################
################# Blog Index Page ################################
##################################################################

class BlogIndexPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('willys_website.BlogIndexPage', related_name='related_links')


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
    ]

    @property
    def blogs(self):
        # Get list of live blog pages that are descendants of this page
        blogs = BlogPage.objects.live().descendant_of(self)

        # Order by most recent date first
        blogs = blogs.order_by('-date')

        return blogs

    def get_context(self, request):
        # Get blogs
        blogs = self.blogs

        # Filter by tag
        tag = request.GET.get('tag')
        if tag:
            blogs = blogs.filter(tags__name=tag)

        # Pagination
        page = request.GET.get('page')
        paginator = Paginator(blogs, 10)  # Show 10 blogs per page
        try:
            blogs = paginator.page(page)
        except PageNotAnInteger:
            blogs = paginator.page(1)
        except EmptyPage:
            blogs = paginator.page(paginator.num_pages)

        # Update template context
        context = super(BlogIndexPage, self).get_context(request)
        context['blogs'] = blogs
        return context

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        InlinePanel('related_links', label="Related links"),
    ]

    promote_panels = Page.promote_panels

##################################################################
################# Blog Page ######################################
##################################################################

class BlogPageHeroItem(Orderable, HeroItem):
    page = ParentalKey('willys_website.BlogPage', related_name='hero')


class BlogPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('willys_website.BlogPage', related_name='related_links')


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey('willys_website.BlogPage', related_name='tagged_items')


class BlogPage(Page):
    body = StreamField(BlogStreamBlock())
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    date = models.DateField("Post date")
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    @property
    def blog_index(self):
        # Find closest ancestor which is a blog index
        return self.get_ancestors().type(BlogIndexPage).last()

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        StreamFieldPanel('body'),
        InlinePanel('hero', label="Hero"),
        InlinePanel('related_links', label="Related links"),
    ]

    promote_panels = Page.promote_panels + [
        ImageChooserPanel('feed_image'),
        FieldPanel('tags'),
    ]

##################################################################
################# Event Page #####################################
##################################################################

class EventPageHeroItem(Orderable, HeroItem):
    page = ParentalKey('willys_website.EventPage', related_name='hero')


class EventPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('willys_website.EventPage', related_name='related_links')

class EventPage(Page):
    date_from = models.DateField("Start date")
    date_to = models.DateField(
        "End date",
        null=True,
        blank=True,
        help_text="Not required if event is on a single day"
    )
    time_from = models.TimeField("Start time", null=True, blank=True)
    time_to = models.TimeField("End time", null=True, blank=True)
    location = models.CharField(max_length=255)
    body = RichTextField(blank=True)
    cost = models.CharField(max_length=255)
    signup_link = models.URLField(blank=True)
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    @property
    def event_index(self):
        # Find closest ancestor which is an event index
        return self.get_ancestors().type(EventIndexPage).last()

    def serve(self, request):
        if "format" in request.GET:
            if request.GET['format'] == 'ical':
                # Export to ical format
                response = HttpResponse(
                    export_event(self, 'ical'),
                    content_type='text/calendar',
                )
                response['Content-Disposition'] = 'attachment; filename=' + self.slug + '.ics'
                return response
            else:
                # Unrecognised format error
                message = 'Could not export event\n\nUnrecognised format: ' + request.GET['format']
                return HttpResponse(message, content_type='text/plain')
        else:
            # Display event page as usual
            return super(EventPage, self).serve(request)

    content_panels = Page.content_panels + [
        FieldPanel('date_from'),
        FieldPanel('date_to'),
        FieldPanel('time_from'),
        FieldPanel('time_to'),
        FieldPanel('location'),
        FieldPanel('cost'),
        FieldPanel('signup_link'),
        InlinePanel('hero', label="Hero"),
        FieldPanel('body', classname="full"),
        InlinePanel('related_links', label="Related links"),
    ]

    promote_panels = Page.promote_panels + [
        ImageChooserPanel('feed_image'),
    ]
