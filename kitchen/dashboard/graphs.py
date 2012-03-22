import os

import pydot
from kitchen.settings import STATIC_ROOT, REPO


def generate_node_map(nodes):
    """Generates a graphviz nodemap"""
    graph = pydot.Dot(graph_type='digraph')
    graph_nodes = {}
    for node in nodes:
        label = node['name'] + "\n" + "\n".join(
            [role for role in node['role'] \
                if not role.startswith(REPO['ENV_PREFIX'])])
        node_el = pydot.Node(label, style="filled", fillcolor="red")
        graph_nodes[node['name']] = node_el
        graph.add_node(node_el)
    for node in nodes:
        for attr in node.keys():
            if isinstance(node[attr], dict) and 'client_roles' in node[attr]:
                for client_node in nodes:
                    if set.intersection(set(node[attr]['client_roles']),
                                        set(client_node['roles'])):
                        graph.add_edge(pydot.Edge(
                            graph_nodes[client_node['name']],
                                graph_nodes[node['name']]))
    keys = graph_nodes.keys()
    graph.add_edge(pydot.Edge(graph_nodes[keys[3]], graph_nodes[keys[5]]))
    graph.write_png(os.path.join(STATIC_ROOT, 'img', 'node_map.png'))
