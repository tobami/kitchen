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
        log.error("Couldn't find {0}. ".format(missing_str(missing)))
        return False
    else:
        return True


def load_nodes():
    if not check_kitchen():
        return []
    current_dir = os.getcwd()
    os.chdir(KITCHEN_DIR)
    nodes = []
    try:
        nodes = lib.get_nodes()
    except SystemExit as e:
        log.error(e)
    finally:
        os.chdir(current_dir)
    return nodes


def load_roles():
    if not check_kitchen():
        return []
    current_dir = os.getcwd()
    os.chdir(KITCHEN_DIR)
    nodes = []
    try:
        nodes = lib.get_roles()
    except SystemExit as e:
        log.error(e)
    finally:
        os.chdir(current_dir)
    return nodes


def get_roles():
    return load_roles()


def get_nodes():
    return load_nodes()
