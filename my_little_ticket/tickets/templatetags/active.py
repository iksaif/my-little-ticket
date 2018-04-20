"""Active template tag."""
import re

from django import template
from django.urls.resolvers import NoReverseMatch
from django.urls.base import reverse

register = template.Library()


@register.simple_tag(takes_context=True)
def active(context, pattern_or_urlname):
    """Return 'active' if the current request matches the pattern."""
    try:
        pattern = "^" + reverse(pattern_or_urlname)
    except NoReverseMatch:
        pattern = pattern_or_urlname
    path = context["request"].path
    if re.search(pattern, path):
        return "active"

    return ""
