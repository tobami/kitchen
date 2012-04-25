"""Dashboard template filters"""
from django import template

from kitchen.settings import REPO

register = template.Library()


@register.filter(name='is_environment_role')
def is_environment_role(string):
    """Returns true if string begins with excluded role prefixes"""
    return string.startswith(REPO['EXCLUDE_ROLE_PREFIX'])
