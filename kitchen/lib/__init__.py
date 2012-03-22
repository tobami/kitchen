import os
import json

from kitchen.settings import KITCHEN_LOCATION

def load_data(data_type):
    retval = []
    nodes_dir = os.path.join(KITCHEN_LOCATION, data_type)
    if not os.path.isdir(nodes_dir):
        raise IOError('Invalid data type or kitchen location. Check your settings.')
    for filename in os.listdir(nodes_dir):
        if filename.endswith('.json'):
            entry = {'name': filename[:-5]}
            f = open(os.path.join(nodes_dir, filename), 'r')
            entry['data'] = json.load(f)
            f.close()
            retval.append(entry)
    return sort_list_by_data_key(retval, 'chef_environment')

def sort_list_by_data_key(old_list, key):
    return sorted(old_list, key=lambda k: k['data'][key]) 