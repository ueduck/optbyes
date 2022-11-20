import networkx as nx

import optbyes as opb

__all__ = [
    "convert_team_priority_to_team_priority_array",
    "convert_team_priority_to_edges",
    "convert_team_priority_to_graph",
]


def convert_team_priority_to_team_priority_array(team_priority: opb.TeamPriority) -> opb.TeamPriorityArray:
    """Generate TeamPriorityArray from team_priority

    Generate parameters such that 1 if team k plays team i before team j
    (team_priority_array[k, i, j] = 1), 0 otherwise.

    Parameters
    -----
    team_priority: opb.TeamPriority
        A dictionary of the team's desired priority order

    Returns
    -----
    team_priority_array: opb.TeamPriorityArray
        Parameters such that 1 if team k plays team i before team j
        (team_priority_array[k, i, j] = 1), 0 otherwise.
    """
    team_priority_array: opb.TeamPriorityArray = {}
    # for team k, team i -> team j => sequence[k, i, j] = 1
    for team_k, seq in team_priority.items():
        for i in range(len(seq) - 1):
            team_i = seq[i]
            for j in range(i + 1, len(seq)):
                team_j = seq[j]
                team_priority_array[team_k, team_i, team_j] = 1
    # otherwise
    for t in team_priority.keys():
        for i in team_priority.keys():
            for j in team_priority.keys():
                try:
                    team_priority_array[t, i, j]
                except KeyError:
                    team_priority_array[t, i, j] = 0
    return team_priority_array


def convert_team_priority_to_edges(team_priority: opb.TeamPriority) -> list[opb.OpbEdge]:
    """Create an edge set based on the team_priority

    Prameters
    -----
    team_priority: opb.TeamPriority
        A dictionary of the team's desired priority order

    Returns
    -----
    edges: list[opb.OpbEdge]
        edge set expressing team_priority

    Examples
    -----
    >>> team_priority = {1: (2, 3), 2: (1, 3), 3: (1, 2)}
    >>> _generate_edges(team_priority)
    >>> [((1, 2), (1, 3)), ((1, 2), (2, 3)), ((1, 3), (2, 3))]
    """
    edges: list[opb.OpbEdge] = []
    for t, opposing_teams in team_priority.items():
        num_opposing_teams = len(opposing_teams)
        for i in range(num_opposing_teams - 1):  # 1 <= i + 1 <= num_teams_1
            pred_node, succ_node = opposing_teams[i], opposing_teams[i + 1]
            start_node = (min(t, pred_node), max(t, pred_node))
            end_node = (min(t, succ_node), max(t, succ_node))
            edges.append((start_node, end_node))
    return edges


def convert_team_priority_to_graph(team_priority: opb.TeamPriority) -> nx.DiGraph:
    """Create directed graph expressing team_priority

    Parameters
    -----
    team_priority: opb.TeamPriority
        A dictionary of the team's desired priority order

    Returns
    -----
    G: nx.DiGraph
        Directed graph expressing team_priority
    """
    G = nx.DiGraph()
    num_teams = len(team_priority)
    nodes = [(i, j) for i in range(1, num_teams) for j in range(i + 1, num_teams + 1)]
    G.add_nodes_from(nodes, color=opb.NODE_COLOR)
    edges = convert_team_priority_to_edges(team_priority)
    G.add_edges_from(edges, color=opb.EDGE_COLOR)
    return G
