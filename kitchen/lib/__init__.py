import os
import json

from kitchen.settings import REPO, REPO_BASE_PATH, KITCHEN_DIR


def load_data(data_type):
    retval = []
    data_dir = os.path.join(KITCHEN_DIR, data_type)
    if not os.path.isdir(data_dir):
        raise IOError(
            'Invalid data type or kitchen location. Check your settings.')
    for filename in os.listdir(data_dir):
        if filename.endswith('.json'):
            entry = {'name': filename[:-5]}
            f = open(os.path.join(data_dir, filename), 'r')
            entry['data'] = json.load(f)
            f.close()
            retval.append(entry)
    return sort_list_by_data_key(retval, 'chef_environment')


def sort_list_by_data_key(old_list, key):
    return sorted(old_list, key=lambda k: k['data'][key]) 
