import os
import json

from littlechef import runner, lib
from logbook import Logger, MonitoringFileHandler

from kitchen.settings import REPO, REPO_BASE_PATH, KITCHEN_DIR, LOG_FILE


file_log_handler = MonitoringFileHandler(LOG_FILE, bubble=False)
file_log_handler.push_application()
log = Logger('kitchen.lib')


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


def load_data(data_type):
    if not check_kitchen():
        return []
    current_dir = os.getcwd()
    os.chdir(KITCHEN_DIR)
    nodes = []
    if data_type not in ["nodes", "roles"]:
        log.error("Unsupported data type '{0}'".format(data_type))
        return nodes
    try:
        nodes = getattr(lib, "get_" + data_type)()
    except SystemExit as e:
        log.error(e)
    finally:
        os.chdir(current_dir)
    return nodes


def get_nodes():
    return load_data("nodes")


def get_roles():
    return load_data("roles")
