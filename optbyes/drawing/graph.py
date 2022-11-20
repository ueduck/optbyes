"""
Draw graph with networkx (and matplotlib)

Examples
-----
>>> G = nx.DiGraph()
>>> edges = [((1, 2), (1, 3)), ((1, 3), (1, 4))]
>>> G.add_edges_from(edges)
>>> pos = opb.decide_layout(G)
>>> opb.draw_graph(G)

See Also
-----
    - :func:`networkx.draw_networkx()`
    - :func:`networkx.topological_generations()`
    - :func:`networkx.multipartite_layout()`
    - :func:`networkx.planar_layout()`
    - :class:`matplotlib.animation.FuncAnimation`
"""

from inspect import signature

import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.animation import FuncAnimation, TimedAnimation

import optbyes as opb

__all__ = [
    "decide_layout",
    "draw_graph",
    "draw_simulation",
]


def decide_layout(graph: nx.Graph) -> opb.Pos:
    """Position nodes on a topological or planar

    Parameters
    -----
    graph: nx.DiGraph
        A networkx directed graph

    Returns
    -----
    pos: dict[opt.OptNode, opb.Pos]
        Position nodes
    """
    pos: opb.Pos = {}
    try:
        for layer, nodes in enumerate(nx.topological_generations(graph)):
            for node in nodes:
                graph.nodes[node]["layer"] = layer
        pos = nx.multipartite_layout(graph, subset_key="layer")
    except nx.NetworkXUnfeasible:  # when Graph is NOT DAG
        pos = nx.planar_layout(graph)
    return pos


def draw_graph(graph: nx.DiGraph, pos: opb.Pos | None = None, **kwargs) -> None:  # type: ignore
    """Draw the graph using networkx.draw_networkx()

    Draw the graph with networkx with options for node positions, labeling, titles,
    and many other drawing features.

    Parameters
    -----
    graph: nx.DiGraph
        A networkx directed graph

    pos: dictionary | None, optional (default = None)
        A dictionary with nodes as keys and positions as values.
        If not specified, try to use a topological layout (with :meth:`networkx.topological_generations()`).
        When the graph is not DAG, a :meth:`networkx.planar_layout()` positioning will be computed.

    kwargs: other keyword arguments
        All other keyword arguments are passed to :meth:`networkx.draw_networkx()`

    Examples
    -----
    >>> draw_graph(G, pos=nx.spring_layout(G))  # use spring layout

    Also see the NetworkX drawing examples at
    https://networkx.org/documentation/latest/auto_examples/index.html
    """
    valid_node_kwargs = signature(nx.draw_networkx_nodes).parameters.keys()
    valid_edge_kwargs = signature(nx.draw_networkx_edges).parameters.keys()
    valid_label_kwargs = signature(nx.draw_networkx_labels).parameters.keys()

    # Create a set with all valid keywords across the three functions
    # and remove the arguments of this function (draw_networkx)
    valid_kwargs = (valid_node_kwargs | valid_edge_kwargs | valid_label_kwargs) - {
        "G",
        "pos",
        "arrows",
        "with_labels",
    }

    if any([k not in valid_kwargs for k in kwargs]):
        invalid_args = ", ".join([k for k in kwargs if k not in valid_kwargs])
        raise ValueError(f"Received invalid argument(s): {invalid_args}")

    # pos
    if pos is None:
        pos = decide_layout(graph)

    # options
    try:
        node_colors = [n["color"] for n in graph.nodes.values()]
        edge_colors = [e["color"] for e in graph.edges.values()]
        kwargs.setdefault("node_color", node_colors)
        kwargs.setdefault("edge_color", edge_colors)
    except KeyError:
        pass
    kwargs.setdefault("node_size", 1200)
    kwargs.setdefault("connectionstyle", "arc3, rad=0.6")

    nx.draw_networkx(graph, pos, **kwargs)


def draw_simulation(filename: str, graph: nx.DiGraph, **kwargs) -> None:  # type: ignore
    """Draw the simulation of match situations

    Parameters
    -----
    filename: str
        The output filename, e.g., :file:`sample.gif`
    graph: nx.DiGraph
        A networkx directed (acyclic) graph
    """
    valid_drawnx_kwargs = signature(draw_graph).parameters.keys()
    valid_fcanim_kwargs = signature(FuncAnimation.__init__).parameters.keys()
    valid_tdanim_kwargs = signature(TimedAnimation.__init__).parameters.keys()
    valid_kwargs = valid_drawnx_kwargs | valid_fcanim_kwargs | valid_tdanim_kwargs

    if any([k not in valid_kwargs for k in kwargs]):
        invalid_args = ", ".join([k for k in kwargs if k not in valid_kwargs])
        raise ValueError(f"Received invalid argument(s): {invalid_args}")

    drawnx_kwargs = {k: v for k, v in kwargs.items() if k in valid_drawnx_kwargs}
    tdanim_kwargs = {k: v for k, v in kwargs.items() if k in valid_tdanim_kwargs}
    fcanim_kwargs = {k: v for k, v in kwargs.items() if k in valid_fcanim_kwargs}
    fcanim_kwargs.update(tdanim_kwargs)
    num_nodes = len(graph.nodes())
    fcanim_kwargs.setdefault("frames", num_nodes + 1)

    copied_graph = graph.copy()
    pos = decide_layout(copied_graph)

    def _update(n: int) -> None:
        ax.clear()
        ax.set_xlim(-1.25, 1.25)  # Allow a little white space on the left and right sides
        ax.set_ylim(-1, 1)
        ax.axis("off")
        if n < 2:  # The 1st frame of the gif displays the initial state
            draw_graph(copied_graph, **drawnx_kwargs)
            return
        for node, indegree in list(copied_graph.in_degree()):  # type: ignore
            if indegree != 0:
                continue
            copied_graph.remove_node(node)
            copied_graph.add_nodes_from([(node, {"color": "#FFFFFF"})])
        draw_graph(copied_graph, pos, **drawnx_kwargs)

    fig = plt.figure(figsize=(8.27, 11.69), tight_layout=True)
    ax = fig.add_subplot(1, 1, 1)
    anim = FuncAnimation(fig, _update, **fcanim_kwargs)
    anim.save(filename, writer="pillow")
