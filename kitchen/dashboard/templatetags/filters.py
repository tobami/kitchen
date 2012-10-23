"""Dashboard template filters"""
from django import template
import littlechef

from kitchen.settings import REPO

register = template.Library()


@register.filter(name='get_role_list')
def get_role_list(run_list):
    """Returns the role sublist from the given run_list"""
    if run_list:
        all_roles = littlechef.lib.get_roles_in_node(
            {'run_list': run_list})
        role_list = []
        for role in all_roles:
            if not role.startswith(REPO['EXCLUDE_ROLE_PREFIX']):
                # Only add if it doesn't start with excluded role prefixes
                role_list.append(role)
        return role_list
    else:
        return []


@register.filter(name='get_recipe_list')
def get_recipe_list(run_list):
    """Returns the recipe sublist from the given run_list"""
    return littlechef.lib.get_recipes_in_node({'run_list': run_list} or [])
