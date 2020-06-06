from wagtail.core import blocks

class LinkValue(blocks.StructValue):
    """additional logic for our links"""

    def url(self) -> str:
        internal_page = self.get("internal_page")
        external_link = self.get("external_link")
        if internal_page:
            return internal_page.url
        elif external_link:
            return external_link
        return ""

from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList

class Link(blocks.StructBlock):
    link_text = blocks.CharBlock(
        max_length=50,
        default="More Detail",
    )
    internal_page = blocks.PageChooserBlock(
        required=False,
    )
    external_link = blocks.URLBlock(
        required=False,
    )

    class Meta:
        value_class = LinkValue

    def clean(self, value):
        internal_page = value.get("internal_page")
        external_page = value.get("external_link")
        errors = {}
        if internal_page and external_page:
            errors["internal_page"] = ErrorList(["Both of these fields cannot be filled. Please select or enter one option"])
            errors["external_link"] = ErrorList(["Both of these fields cannot be filled. Please select or enter one option"])
        elif not internal_page and not external_page:
            errors["internal_page"] = ErrorList(["Please select a page or enter a URL for one of these options"])
            errors["external_link"] = ErrorList(["Please select a page or enter a URL for one of these options"])

        if errors:
            raise ValidationError("Validation error in your link",params=errors)

        return super().clean(value)