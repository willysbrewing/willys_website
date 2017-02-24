from datetime import date

from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.utils.encoding import python_2_unicode_compatible
from django import forms
from django.shortcuts import render
from django.core.validators import RegexValidator

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, FieldRowPanel, MultiFieldPanel, \
    InlinePanel, PageChooserPanel, StreamFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtailmedia.edit_handlers import MediaChooserPanel
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
    quote = TextBlock('quote title')
    attribution = CharBlock()

    class Meta:
        icon = 'openquote'


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


class AlignedHTMLBlock(StructBlock):
    html = RawHTMLBlock()

    class Meta:
        icon = 'code'


class GenericStreamBlock(StreamBlock):
    h2 = CharBlock(icon='title', classname='title')
    h3 = CharBlock(icon='title', classname='title')
    h4 = CharBlock(icon='title', classname='title')
    intro = RichTextBlock(icon='pilcrow')
    pullquote = PullQuoteBlock()
    paragraph = RichTextBlock(icon='pilcrow')
    image = ImageBlock(icon='image', label='image')
    html = AlignedHTMLBlock(icon='code', label='html')

##################################################################
########### Abstract classes #####################################
##################################################################

class LinkFields(models.Model):
    link_external = models.URLField('External link', blank=True)
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
        elif self.link_external:
            return self.link_external
        else:
            return '/'

    panels = [
        PageChooserPanel('link_page'),
        FieldPanel('link_external'),
    ]

    # DocumentChooserPanel('link_document'),
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
        ImageChooserPanel('background'),
        MultiFieldPanel(LinkFields.panels, 'Link'),
    ]

##################################################################
################# RelatedLink ####################################
##################################################################

class RelatedLink(LinkFields):
    title = models.CharField(max_length=255, help_text='Link title')

    panels = [
        FieldPanel('title'),
        MultiFieldPanel(LinkFields.panels, 'Link'),
    ]

    class Meta:
        abstract = True

##################################################################
################# HomePage #######################################
##################################################################

class HomePageHero(Orderable, HeroItem):
    page = ParentalKey('willys_website.HomePage', related_name='hero')

class HomePagePromo(Orderable, LinkFields):
    page = ParentalKey('willys_website.HomePage', related_name='promo')
    text = models.CharField(max_length=255)
    color = models.CharField(
        max_length=7,
        null=True,
        blank=True,
        validators=[RegexValidator(regex='^#(?:[0-9a-fA-F]{3}){1,2}$')],
        help_text='Background Color Hex #ffffff')

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
    #parent_page_types = [] # Nothing can have a homepage as a child

    video = models.ForeignKey(
        'wagtailmedia.Media',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    @property
    def feed_image(self):
        return self.hero.all()[0].background

    class Meta:
        verbose_name = 'Homepage'

    content_panels = Page.content_panels + [
        InlinePanel('hero', label='Hero'),
        InlinePanel('promo', label='Promo'),
        InlinePanel('featured', label='Featured'),
        MediaChooserPanel('video'),
    ]

    promote_panels = Page.promote_panels


##################################################################
################# Standard Page ##################################
##################################################################

class StandardPageHeroItem(Orderable, HeroItem):
    page = ParentalKey('willys_website.StandardPage', related_name='hero')

class StandardPage(Page):
    parent_page_types = ['willys_website.HomePage']
    subpage_types = [] # No Children

    body = StreamField(GenericStreamBlock())

    @property
    def feed_image(self):
        return self.hero.all()[0].background

    content_panels = Page.content_panels + [
        InlinePanel('hero', label='Hero'),
        StreamFieldPanel('body'),
    ]

    promote_panels = Page.promote_panels

##################################################################
################# Blog Index Page ################################
##################################################################

class BlogIndexPageHero(Orderable, HeroItem):
    page = ParentalKey('willys_website.BlogIndexPage', related_name='hero')

class BlogIndexPage(Page):
    parent_page_types = ['willys_website.HomePage']
    subpage_types = ['willys_website.BlogPage'] # Children can only be BlogPage

    @property
    def blog_posts(self):
        # Get list of blog pages that are descendants of this page
        blog_posts= BlogPage.objects.live().descendant_of(self)

        # Order by most recent date first
        blog_posts = blog_posts.order_by('-date')
        return blog_posts

    @property
    def feed_image(self):
        return self.hero.all()[0].background

    def get_context(self, request):
        # Get blogs
        blog_posts = self.blog_posts

        # Filter by tag
        tag = request.GET.get('tag')
        if tag:
            blog_posts = blog_posts.filter(tags__name=tag)

        # Pagination
        page = request.GET.get('page')
        paginator = Paginator(blog_posts, 10)  # Show 10 blogs per page
        try:
            blog_posts = paginator.page(page)
        except PageNotAnInteger:
            blog_posts = paginator.page(1)
        except EmptyPage:
            blog_posts = paginator.page(paginator.num_pages)

        # Update template context
        context = super(BlogIndexPage, self).get_context(request)
        context['blog_posts'] = blog_posts
        return context

    content_panels = Page.content_panels + [
        InlinePanel('hero', label='Hero'),
    ]

    promote_panels = Page.promote_panels

##################################################################
################# Blog Page ######################################
##################################################################

class BlogPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('willys_website.BlogPage', related_name='related_links')

class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey('willys_website.BlogPage', related_name='tagged_items')

class BlogPage(Page):
    parent_page_types = ['willys_website.BlogIndexPage'] # Parent can only be a BlogIndex
    subpage_types = [] # No Children

    body = StreamField(GenericStreamBlock())
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    date = models.DateField('Post date')
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    @property
    def hero(self):
        hero = [{'title': self.title, 'background': self.image}]
        return hero

    @property
    def feed_image(self):
        return self.hero[0].get('background')

    @property
    def blog_index(self):
       # Find blog index in ancestors
       for ancestor in reversed(self.get_ancestors()):
           if isinstance(ancestor.specific, BlogIndexPage):
               return ancestor

       # No ancestors are blog indexes,
       # just return first blog index in database
       return BlogIndexPage.objects.first()

    content_panels = Page.content_panels + [
        ImageChooserPanel('image'),
        FieldPanel('date'),
        StreamFieldPanel('body'),
        InlinePanel('related_links', label='Related links'),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel('tags'),
    ]

##################################################################
################# Event Index Page ###############################
##################################################################

class EventIndexPageHero(Orderable, HeroItem):
    page = ParentalKey('willys_website.EventIndexPage', related_name='hero')

class EventIndexPage(Page):
    parent_page_types = ['willys_website.HomePage']
    subpage_types = ['willys_website.EventPage'] # Children can only be EventPage

    @property
    def events(self):
        # Get list of live event pages that are descendants of this page
        events = EventPage.objects.live().descendant_of(self)

        # Filter events list to get ones that are either
        # running now or start in the future
        events = events.filter(date_from__gte=date.today())

        # Order by date
        events = events.order_by('date_from')

        return events

    @property
    def feed_image(self):
        return self.hero.all()[0].background

    content_panels = Page.content_panels + [
        InlinePanel('hero', label='Hero'),
    ]

    promote_panels = Page.promote_panels

##################################################################
################# Event Page #####################################
##################################################################

class EventPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('willys_website.EventPage', related_name='related_links')

class EventPage(Page):
    parent_page_types = ['willys_website.EventIndexPage'] # Parent can only be a EventIndex
    subpage_types = [] # No Children

    date_from = models.DateField('Start date')
    time_from = models.TimeField('Start time', default=None)
    location = models.CharField(max_length=255)
    body = StreamField(GenericStreamBlock())
    cost = models.CharField(max_length=255)
    signup_link = models.URLField(blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    @property
    def hero(self):
        hero = [{'title': self.title, 'background': self.image}]
        return hero

    @property
    def feed_image(self):
        return self.hero[0].get('background')        

    @property
    def event_index(self):
        # Find closest ancestor which is an event index
        return self.get_ancestors().type(EventIndexPage).last()

    content_panels = Page.content_panels + [
        ImageChooserPanel('image'),
        FieldPanel('date_from'),
        FieldPanel('time_from'),
        FieldPanel('location'),
        FieldPanel('cost'),
        StreamFieldPanel('body'),
        FieldPanel('signup_link'),
        InlinePanel('related_links', label='Related links'),
    ]

    promote_panels = Page.promote_panels

##################################################################
################# Product Index Page #############################
##################################################################

class ProductIndexPageHero(Orderable, HeroItem):
    page = ParentalKey('willys_website.ProductIndexPage', related_name='hero')

class ProductIndexPage(Page):
    parent_page_types = ['willys_website.HomePage']
    subpage_types = ['willys_website.ProductPage'] # Children can only be ProductPage

    @property
    def products(self):
        # Get list of live event pages that are descendants of this page
        products = ProductPage.objects.live().descendant_of(self)
        return products

    @property
    def feed_image(self):
        return self.hero.all()[0].background

    content_panels = Page.content_panels + [
        InlinePanel('hero', label='Hero'),
    ]

    promote_panels = Page.promote_panels

##################################################################
################# Product Page ###################################
##################################################################

class ProductPageHero(Orderable, HeroItem):
    page = ParentalKey('willys_website.ProductPage', related_name='hero')

class ProductPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('willys_website.ProductPage', related_name='related_links')

class ProductPage(Page):
    parent_page_types = ['willys_website.ProductIndexPage'] # Parent can only be a ProductIndex
    subpage_types = [] # No Children

    name = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, default='notset')
    bg_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    image = models.ForeignKey(
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
        help_text='Background Color Hex #ffffff')
    style = models.CharField(max_length=255, default='notset')
    proof = models.CharField(max_length=255, default='notset')
    ibu = models.CharField(max_length=255, default='notset')
    price = models.CharField(max_length=255)

    body = StreamField(GenericStreamBlock())

    @property
    def new_hero(self):
        hero = [{
            'name': self.name,
            'subtitle': self.subtitle,
            'bg_image': self.bg_image,
            'image': self.image,
            'color': self.color,
            'style': self.style,
            'proof': self.proof,
            'ibu': self.ibu,
            'price': self.price
            }]
        return hero

    @property
    def product_index(self):
        return self.get_ancestors().type(ProductIndexPage).last()

    @property
    def feed_image(self):
        return self.bg_image

    content_panels = Page.content_panels + [
        FieldPanel('name'),
        FieldPanel('subtitle'),
        ImageChooserPanel('image'),
        ImageChooserPanel('bg_image'),
        FieldPanel('color'),
        FieldPanel('style'),
        FieldPanel('proof'),
        FieldPanel('ibu'),
        FieldPanel('price'),
        StreamFieldPanel('body'),
        InlinePanel('related_links', label='Related links'),
    ]

    promote_panels = Page.promote_panels

##################################################################
################# Landing Page ###################################
##################################################################

class LandingPageHero(Orderable, HeroItem):
    page = ParentalKey('willys_website.LandingPage', related_name='hero')


class LandingPage(Page):
    parent_page_types = ['willys_website.HomePage']
    subpage_types = [] # No Children

    nav = False

    body = StreamField(GenericStreamBlock())

    @property
    def feed_image(self):
        return self.hero.all()[0].background

    content_panels = Page.content_panels + [
        InlinePanel('hero', label='Hero'),
        StreamFieldPanel('body'),
    ]

    promote_panels = Page.promote_panels
