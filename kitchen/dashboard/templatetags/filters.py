"""Dashboard template filters"""
from django import template
import littlechef

from kitchen.settings import REPO, TAG_CLASSES

register = template.Library()


@register.filter(name='get_role_list')
def get_role_list(run_list):
    """Returns the role sublist from the given run_list"""
    role_list = []
    for role in littlechef.lib.get_roles_in_node({'run_list': run_list or []}):
        if not role.startswith(REPO['EXCLUDE_ROLE_PREFIX']):
            # Only add if it doesn't start with excluded role prefixes
            role_list.append(role)
    return role_list


@register.filter(name='get_recipe_list')
def get_recipe_list(run_list):
    """Returns the recipe sublist from the given run_list"""
    return littlechef.lib.get_recipes_in_node({'run_list': run_list or []})


@register.filter(name='get_memory_in_GB')
def get_memory_in_GB(memory_str):
    """Returns the memory value in GB from a given string in kB"""
    try:
        return '{0} GB'.format(int(memory_str[:-2]) / 1000000)
    except (ValueError, TypeError):
        return ''


@register.filter(name='get_cpus')
def get_cpus(cpus):
    return cpus if cpus is not None else "-"


@register.filter(name='get_tag_class')
def get_tag_class(tag):
    """Returns a button class for the given tag"""
    btn_class = TAG_CLASSES.get(tag, "")
    if btn_class == "":
        for key in TAG_CLASSES:
            if key.endswith("*") and tag.startswith(key[:-1]):
                    return TAG_CLASSES[key]
    return btn_class


@register.filter(name='get_link')
def get_link(link):
    """Returns an image link"""
    if not link.get('url'):
        return ""
    elif link.get('img'):
        return ('<a href="{0}" target="_blank" title="{1}" class="btn-custom">'
                '<img width="25" height="25" src="{2}">'
                '</a>'.format(link['url'], link['title'], link['img']))
    elif link.get('title'):
        return ('<a href="{0}" target="_blank" title="{1}" class="btn btn-small btn-custom">{1}'
               '</a>'.format(link['url'], link['title']))
    else:
        return ""
