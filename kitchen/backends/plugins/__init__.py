"""Plugins package"""
from kitchen.backends.plugins.loader import import_plugins


def is_view(func):
    func.__is_view__ = True
    return func

plugins = import_plugins()
