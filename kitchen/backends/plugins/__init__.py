"""Plugins package"""
from kitchen.backends.plugins.loader import import_plugins


def is_view(plugin_type):
    """Decorator to mark a plugin method as being a view.
    Views can be called via the '/plugins/' interface of kitchen and should
    either return None or a proper Django HTTPResponse object

    """
    if callable(plugin_type):
        plugin_type.__is_view__ = True
        plugin_type.__p_type__ = 'list'
        return plugin_type
    else:
        def inner(func):
            func.__is_view__ = True
            func.__p_type__ = plugin_type
            return func
        return inner

plugins = import_plugins()
