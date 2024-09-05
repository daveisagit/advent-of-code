"""Graph visualisation"""

from pyvis.network import Network


def visualize_graph(gph):
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
