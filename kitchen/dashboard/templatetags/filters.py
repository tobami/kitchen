from django.template.defaultfilters import stringfilter
from django import template

from kitchen.settings import REPO

register = template.Library()


@register.filter(name='is_environment_role')
def is_environment_role(string):
    return string.startswith(REPO['EXCLUDE_ROLE_PREFIX'])
