"""Plugin loading facility"""
from kitchen.settings import ENABLE_PLUGINS

plugins = {}
for name in ENABLE_PLUGINS:
    try:
        plugins['name'] = __import__(name)
    except ImportError as e:
        continue
