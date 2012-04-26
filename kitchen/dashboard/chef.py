"""Functions to read and process data from a Chef repository"""
import os
import simplejson as json

from littlechef import runner, lib, chef
from logbook import Logger, MonitoringFileHandler

from kitchen.settings import DEBUG, REPO, REPO_BASE_PATH, LOG_FILE


file_log_handler = MonitoringFileHandler(LOG_FILE, bubble=DEBUG)
file_log_handler.push_application()
log = Logger('kitchen.lib')

KITCHEN_DIR = os.path.join(
    REPO_BASE_PATH, REPO['NAME'], REPO['KITCHEN_SUBDIR'])
DATA_BAG_PATH = os.path.join(KITCHEN_DIR, "data_bags", "node")


class RepoError(Exception):
    """An error related to repository validity"""
    pass


def _check_kitchen():
    """Checks whether there is a valid Chef repository"""
    if not os.path.exists(KITCHEN_DIR):
        raise RepoError("Repo dir doesn't exist at '{0}'".format(KITCHEN_DIR))

    current_dir = os.getcwd()
    os.chdir(KITCHEN_DIR)
    in_a_kitchen, missing = runner._check_appliances()
    os.chdir(current_dir)
    if not in_a_kitchen:
        missing_str = lambda m: ' and '.join(', '.join(m).rsplit(', ', 1))
        raise RepoError("Couldn't find {0}. ".format(missing_str(missing)))
    elif not os.path.exists(DATA_BAG_PATH):
        raise RepoError("Node data bag has not yet been built")
    else:
        return True


def build_node_data_bag():
    """Tells LittleChef to build the node data bag"""
    current_dir = os.getcwd()
    os.chdir(KITCHEN_DIR)
    try:
        lib.get_recipes()  # This builds metadata.json for all recipes
        chef._build_node_data_bag()
    except SystemExit as e:
        log.error(e)
    finally:
        os.chdir(current_dir)
    return True


def get_environments(nodes):
    """Returns an environments set out of chef_environment values found"""
    envs = set()
    counts = {}
    for node in nodes:
        env = node.get('chef_environment', 'none')
        envs.add(env)
        counts.setdefault(env, 0)
        counts[env] += 1
    return [{'name': env, 'counts': counts[env]} for env in sorted(envs)]


def _load_data(data_type):
    """Loads the kitchen's node files"""
    _check_kitchen()
    current_dir = os.getcwd()
    os.chdir(KITCHEN_DIR)
    data = []
    if data_type not in ["nodes", "roles"]:
        log.error("Unsupported data type '{0}'".format(data_type))
        return data
    try:
        data = getattr(lib, "get_" + data_type)()
    except SystemExit as e:
        log.error(e)
    finally:
        os.chdir(current_dir)
    return data


def _load_extended_node_data(nodes):
    """Loads JSON node files from node databag, which has merged attributes"""
    data = []
    for node in nodes:
        # Read corresponding data bag item for each node
        filename = node['name'].replace(".", "_") + ".json"
        filepath = os.path.join(DATA_BAG_PATH, filename)
        if not os.path.exists(filepath):
            error = "'node' data bag was not generated correctly: item "
            error += "'data_bag/node/{0}' is missing".format(filename)
            raise RepoError(error)
        with open(filepath, 'r') as f:
            try:
                data.append(json.loads(f.read()))
            except json.JSONDecodeError as e:
                error = 'LittleChef found the following error in'
                error += ' "{0}":\n {1}'.format(filepath, str(e))
                raise RepoError(error)
    return data


def filter_nodes(nodes, env='', roles='', virt_roles=''):
    """Returns nodes which fulfill env, roles and virt_roles criteria"""
    retval = []
    if roles:
        roles = roles.split(',')
    if virt_roles:
        virt_roles = virt_roles.split(',')
    for node in nodes:
        append = True
        if env and node.get('chef_environment', 'none') != env:
            append = False
        if roles:
            if not set.intersection(set(roles),
                    set([role.split("_")[0] for role in node['roles']])):
                append = False
        if virt_roles:
            # Exclude node in two cases:
            #   * the virtualization role is not in the desired virt_roles
            #   * the virtualization role is not defined for the node AND
            #     'guest' is a desired virt_role
            virt_role = node.get('virtualization', {}).get('role')
            if not virt_role in virt_roles and \
                    not ('guest' in virt_roles and not virt_role):
                append = False
        if append:
            retval.append(node)
    return retval


def get_nodes_extended():
    """Returns node data from the automatic 'node' data_bag"""
    return _load_extended_node_data(_load_data("nodes"))


def get_nodes():
    """Returns nodes present in the repository's 'nodes' directory"""
    return _load_data("nodes")


def get_roles():
    """Returns roles present in the repository's 'roles' directory"""
    return _load_data("roles")


def get_role_groups(roles):
    """Compiles a set of role prefixes"""
    groups = set()
    for role in roles:
        split = role['name'].split('_')
        if split[0] != REPO['EXCLUDE_ROLE_PREFIX']:
            groups.add(split[0])
    return sorted(groups)
