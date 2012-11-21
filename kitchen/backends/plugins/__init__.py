"""Plugins package"""
from kitchen.backends.plugins.loader import import_plugins


def is_view(caps=None):
    """Decorator to mark a plugin method as being a view.
    Views can be called via the '/plugins/' interface of kitchen and should
    either return None or a proper Django HTTPResponse object

    """
    if callable(caps):
        caps.__is_view__ = True
        caps.__p_type__ = 'list'
        return caps
    else:
        def inner(func):
            func.__is_view__ = True
            func.__p_type__ = caps
            return func
        return inner

plugins = import_plugins()
