from django.db import models
from django.core.exceptions import ValidationError

from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel

from streams import blocks

from wagtail.images.blocks import ImageChooserBlock
from wagtail.core import blocks as wagtail_blocks

class BlogListingPage(Page):
    # parent_page_types = ["home.HomePage"]
    template = "cmsblog/blog_listing_page.html"
    subtitle = models.TextField(
        blank=True,
        max_length=500,
    )
    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
    ]
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['cmsblog'] = BlogPage.objects.live().public()
        return context

class BlogPage(Page):
    # parent_page_types = ["home.HomePage", "flex.FlexPage"]
    preamble = models.TextField(blank = True)
    body = StreamField([
        ("richtext",wagtail_blocks.RichTextBlock(
            template='streams/simple_richtext_block.html',
        )),
        ("codeblock",wagtail_blocks.RichTextBlock(
            template='streams/code_richtext_block.html',
        )),
        ("large_image",ImageChooserBlock(
            help_text='This image will be cropped to 1200px by 775px',
            template='streams/large_image_block.html',
        )),
        ("link", blocks.Link(
            help_text="Enter a link or select a page"
        )),
    ], null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("preamble"),
        StreamFieldPanel("body"),
    ]