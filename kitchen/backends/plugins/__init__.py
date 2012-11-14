"""Plugins package"""
from kitchen.backends.plugins.loader import import_plugins

plugins = import_plugins()
