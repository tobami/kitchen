import os
import json

from kitchen.settings import KITCHEN_LOCATION

def load_nodes():
    retval = {}
    nodes_dir = os.path.join(KITCHEN_LOCATION, 'nodes')
    for filename in os.listdir(nodes_dir):
        f = open(os.path.join(nodes_dir, filename), 'r')
        retval[filename[:-5]] = json.load(f)
        f.close()
    return retval