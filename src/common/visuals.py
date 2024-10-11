"""Graph visualisation"""

from pyvis.network import Network

from common.graph import all_nodes


def visualize_graph_2019_25(gph):
    """Basic visual"""
    net = Network(height="1200px", width="100%", directed=True)

    for n in gph:
        net.add_node(n)

    for u, edges in gph.items():
        for v, c in edges.items():
            print(c)
            net.add_edge(u, v, weight=1, label=c.get("nav")[:1], title=c.get("nav"))

    net.toggle_physics(True)
    net.show("temp_graph.html", notebook=False)


def visualize_graph(gph, directed=True):
    """Basic visual"""
    net = Network(height="1200px", width="100%", directed=directed)

    for n in all_nodes(gph):
        net.add_node(str(n))

    for u, edges in gph.items():
        for v, c in edges.items():
            net.add_edge(str(u), str(v), weight=1, label=str(c))

    net.toggle_physics(True)
    net.show("temp_graph.html", notebook=False)
