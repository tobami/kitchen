"""Facility to render node graphs using pydot"""
import os
import subprocess
import tempfile
import threading

import pydot
from logbook import Logger

from kitchen.settings import STATIC_ROOT, REPO, COLORS
from kitchen.backends.lchef import get_role_groups

log = Logger(__name__)


def _build_links(nodes):
    """Returns a dictionary of nodes that have links to other nodes
    A node builds its links by looking for other nodes with roles present
    in its 'client_nodes' lists

    """
    linked_nodes = {}
    for node in nodes:
        links = {}
        for attr in node.keys():
            client_roles = []
            try:
                client_roles = node[attr]['client_roles']
            except (TypeError, KeyError):
                pass
            for client_node in nodes:
                if set.intersection(
                        set(client_roles), set(client_node['roles'])):
                    links.setdefault('client_nodes', [])
                    links['client_nodes'].append((client_node['name'], attr))
            needs_roles = []
            try:
                needs_roles = node[attr]['needs_roles']
            except (TypeError, KeyError):
                pass
            for needed_node in nodes:
                if set.intersection(
                        set(needs_roles), set(needed_node['roles'])):
                    links.setdefault('needs_nodes', [])
                    links['needs_nodes'].append((needed_node['name'], attr))
        if (len(links.get('client_nodes', [])) or
                len(links.get('needs_nodes', []))):
            linked_nodes[node['name']] = links
    return linked_nodes


def generate_node_map(nodes, roles, show_hostnames=True):
    """Generates a graphviz node map"""
    graph = KitchenDot(graph_type='digraph')
    clusters = {}
    graph_nodes = {}

    role_colors = {}
    color_index = 0
    role_groups = get_role_groups(roles) + ['none']
    for role in role_groups:
        clusters[role] = pydot.Cluster(
            role, label=role, color=COLORS[color_index], fontsize="12")
        graph.add_subgraph(clusters[role])
        role_colors[role] = COLORS[color_index]
        color_index += 1
        if color_index >= len(COLORS):
            color_index = 0

    # Create nodes
    node_labels = {}  # Only used when show_hostnames = False
    for node in nodes:
        color = "lightyellow"
        try:
            role_prefix = node['role'][0].split("_")[0]
            if role_prefix == REPO['EXCLUDE_ROLE_PREFIX']:
                role_prefix = 'none'
                role_prefix = node['role'][1].split("_")[0]
                if role_prefix == REPO['EXCLUDE_ROLE_PREFIX']:
                    role_prefix = 'none'
            color = role_colors[role_prefix]
        except (IndexError, KeyError):
            role_prefix = 'none'
        label = "\n".join([role for role in node['role']
                          if not role.startswith(REPO['EXCLUDE_ROLE_PREFIX'])])
        if show_hostnames:
            label = node['name'] + "\n" + label
        else:
            if not label:
                label = "norole"
            if label in node_labels:
                if node_labels[label] == 1:
                    first_node = clusters[role_prefix].get_node(label)[0]
                    first_node.set_name(label + " (1)")
                node_labels[label] += 1
                label += " ({0})".format(node_labels[label])
            else:
                node_labels[label] = 1

        node_el = pydot.Node(label,
                             shape="box",
                             style="filled",
                             fillcolor=color,
                             fontsize="9")
        graph_nodes[node['name']] = node_el
        clusters[role_prefix].add_node(node_el)
    links = _build_links(nodes)
    for node in links:
        for client in links[node].get('client_nodes', []):
            edge = pydot.Edge(
                graph_nodes[client[0]],
                graph_nodes[node],
                fontsize="8",
                arrowsize=.6,
            )
            edge.set_label(client[1])
            graph.add_edge(edge)
        for client in links[node].get('needs_nodes', []):
            edge = pydot.Edge(
                graph_nodes[node],
                graph_nodes[client[0]],
                fontsize="7",
                style="dashed",
                arrowsize=.6,
            )
            edge.set_label(client[1])
            graph.add_edge(edge)

    # Generate graph
    filename = os.path.join(STATIC_ROOT, 'img', 'node_map.svg')
    timeout = 10.0  # Seconds
    graph_thread = GraphThread(filename, graph)
    graph_thread.start()
    result = graph_thread.join(timeout)
    if graph_thread.isAlive():
        # Kill the pydot graphviz's subprocess
        graph_thread.kill()
        timeout = int(timeout)
        log.error("pydot timeout: {0} seconds".format(timeout))
        return False, ("Unable to draw graph, timeout exceeded "
                       "({0} seconds)").format(timeout)
    else:
        return result


class GraphThread(threading.Thread):
    """Thread for pydot graph generation. Wraphs the file creation"""

    def __init__(self, filename, graph):
        self.filename = filename
        self.graph = graph
        self._return = False, "Unable to draw graph, unexpected error"
        threading.Thread.__init__(self)

    def run(self):
        try:
            self.graph.write_svg(self.filename)
        except pydot.InvocationException as e:
            log.error("pydot error: {0}".format(str(e)))
            self._return = False, "Unable to render the graph"
        else:
            self._return = True, self.filename

    def join(self, timeout=None):
        threading.Thread.join(self, timeout)
        return self._return

    def kill(self):
        if self.graph.p:
            self.graph.p.kill()


class KitchenDot(pydot.Dot):
    """Inherits from the pydot library Dot class, and makes the subprocess as
    an attribute for being killed from outside

    """
    def __init__(self, *argsl, **argsd):
        super(KitchenDot, self).__init__(*argsl, **argsd)
        self.p = None

    def create(self, prog=None, format='ps'):
        """Creates and returns a Postscript representation of the graph."""
        if prog is None:
            prog = self.prog

        if isinstance(prog, (list, tuple)):
            prog, args = prog[0], prog[1:]
        else:
            args = []

        if self.progs is None:
            self.progs = pydot.find_graphviz()
            if self.progs is None:
                raise pydot.InvocationException(
                    'GraphViz\'s executables not found')

        if not prog in self.progs:
            raise pydot.InvocationException(
                'GraphViz\'s executable "{0}" not found'.format(prog))

        if (not os.path.exists(self.progs[prog])
                or not os.path.isfile(self.progs[prog])):
            raise pydot.InvocationException(
                'GraphViz\'s executable "{0}" is not a file '
                'or doesn\'t exist'.format(self.progs[prog]))

        tmp_fd, tmp_name = tempfile.mkstemp()
        os.close(tmp_fd)
        self.write(tmp_name)
        tmp_dir = os.path.dirname(tmp_name)

        # For each of the image files...
        for img in self.shape_files:
            # Get its data
            f = file(img, 'rb')
            f_data = f.read()
            f.close()

            # Copy it under a file with the same name in the temp dir
            f = file(os.path.join(tmp_dir, os.path.basename(img)), 'wb')
            f.write(f_data)
            f.close()

        cmdline = [self.progs[prog], '-T' + format, tmp_name] + args

        self.p = subprocess.Popen(
            cmdline,
            cwd=tmp_dir,
            stderr=subprocess.PIPE, stdout=subprocess.PIPE
        )

        stderr = self.p.stderr
        stdout = self.p.stdout

        stdout_output = list()
        while True:
            data = stdout.read()
            if not data:
                break
            stdout_output.append(data)
        stdout.close()

        stdout_output = ''.join(stdout_output)

        if not stderr.closed:
            stderr_output = list()
            while True:
                data = stderr.read()
                if not data:
                    break
                stderr_output.append(data)
            stderr.close()

            if stderr_output:
                stderr_output = ''.join(stderr_output)

        status = self.p.wait()

        if status != 0:
            raise pydot.InvocationException(
                'Program terminated with status: {0}. '
                'stderr follows: {1}'.format(status, stderr_output))
        elif stderr_output:
            print stderr_output

        #  For each of the image files...
        for img in self.shape_files:
            #  Remove it
            os.unlink(os.path.join(tmp_dir, os.path.basename(img)))

        os.unlink(tmp_name)

        return stdout_output
