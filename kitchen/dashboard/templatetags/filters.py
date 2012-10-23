"""Dashboard template filters"""
from django import template

from kitchen.settings import REPO

register = template.Library()


@register.filter(name='get_role_list')
def get_role_list(run_list):
    """Returns the role sublist from the given run_list"""
    role_list = []
    if run_list:
        for element in run_list:
            if "role[" in element:
                role = element.split("role[")[1][:-1]
                if not role.startswith(REPO['EXCLUDE_ROLE_PREFIX']):
                    # Only add if it doesn't start with excluded role prefixes
                    role_list.append(role)
    return role_list


@register.filter(name='get_recipe_list')
def get_recipe_list(run_list):
    """Returns the recipe sublist from the given run_list"""
    recipe_list = []
    if run_list:
        for element in run_list:
            if "recipe[" in element:
                recipe_list.append(element.split("recipe[")[1][:-1])
    return recipe_list
