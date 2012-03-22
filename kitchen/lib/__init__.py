import os
import json

from littlechef import runner, lib

from kitchen.settings import REPO, REPO_BASE_PATH, KITCHEN_DIR


def check_kitchen():
    current_dir = os.getcwd()
    os.chdir(KITCHEN_DIR)
    in_a_kitchen, missing = runner._check_appliances()
    os.chdir(current_dir)
    if not in_a_kitchen:
        missing_str = lambda m: ' and '.join(', '.join(m).rsplit(', ', 1))
        return False, "Couldn't find {0}. ".format(missing_str(missing))
    else:
        return True, None


def load_nodes():
    current_dir = os.getcwd()
    os.chdir(KITCHEN_DIR)
    nodes = False
    try:
        nodes = lib.get_nodes()
    except SystemExit:
        pass
    finally:
        os.chdir(current_dir)
    return nodes


def get_nodes():
    in_a_kitchen, msg = check_kitchen()
    if not in_a_kitchen:
        return False, msg

    nodes = load_nodes()
    if not nodes:
        return False, "A node file is not valid JSON"
    else:
        return True, nodes
