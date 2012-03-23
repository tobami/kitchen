import os

import pydot
from kitchen.settings import STATIC_ROOT, REPO


def generate_node_map(nodes):
    """Generates a graphviz nodemap"""
    graph = pydot.Dot(graph_type='digraph')
    graph_nodes = {}
    # Create nodes
    for node in nodes:
        if "xen_host" in node['role']:
            continue
        label = node['name'] + "\n" + "\n".join(
            [role for role in node['role'] \
                if not role.startswith(REPO['ENV_PREFIX'])])
        node_el = pydot.Node(label,
                             style="filled",
                             fillcolor="lightyellow",
                             fontsize="8")
        graph_nodes[node['name']] = node_el
        graph.add_node(node_el)
    # Create links
    for node in nodes:
        for attr in node.keys():
            if isinstance(node[attr], dict) and 'client_roles' in node[attr]:
                for client_node in nodes:
                    if set.intersection(set(node[attr]['client_roles']),
                                        set(client_node['roles'])):
                        edge = pydot.Edge(graph_nodes[client_node['name']],
                                          graph_nodes[node['name']],
                                          fontsize="8")
                        edge.set_label(attr)
                        graph.add_edge(edge)
    # Generate graph
    graph.write_png(os.path.join(STATIC_ROOT, 'img', 'node_map.png'))
