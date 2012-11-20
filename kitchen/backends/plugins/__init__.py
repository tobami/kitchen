"""Plugins package"""
from kitchen.backends.plugins.loader import import_plugins


def is_view(func):
    """Decorater to mark a plugin method as being a view.
    Views can be called via the '/plugins/' insterface of kitchen and should
    either return None or a proper Django HTTPResponse object

    """
    func.__is_view__ = True
    return func

plugins = import_plugins()
