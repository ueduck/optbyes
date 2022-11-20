#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
**********
Experiments
**********

This file contains a collection of code that experiments with the OptimizeByes problem,
enumerating all combinations of priorities, which combinations are feasible, and if so,
how many rounds can be achieved.
"""

import itertools

import optbyes as opb
from optbyes.utils import converter, generator


def experiment_all_combs_with_gurobi(num_teams: int, num_fixed: int = 0) -> None:
    """Experiment with the OptimizeByes problem by Gurobi

    Experiment with the OptimizeByes problem by Gurobi,
    enumerating all combinations of priorities, which combinations are feasible,
    and if so, how many rounds can be achieved.

    Prameters
    -----
    num_teams: int
        The number of teams

    num_fixed: int, optional (default = 0)
        The number of teams fixing priorities.
        Fixes the priority of teams from 1 to num_teams.
    """
    # 1. Test feasible
    cnt = 0
    cnt_feasible = 0
    team_priorities: list[opb.TeamPriority] = generator.generate_team_priorities(num_teams, num_fixed)
    for tp in team_priorities:
        # 1.1 Solve instance
        factory = opb.BaseILPFactory()
        solver = opb.ProbSolverWithGurobi.create_from_team_priority(tp, factory)
        solver.solve()
        if solver.get_status() == opb.OPTIMAL:
            cnt_feasible += 1

        # 1.2 Update
        cnt += 1

    # 2. Print Answer
    print(f"{cnt = }, {cnt_feasible = }")


def experiment_all_combs_with_graph_algorithm(num_teams: int) -> None:
    """Experiment with the OptimizeByes problem by Graph algorithm

    Experiment with the OptimizeByes problem by Graph algorithm,
    enumerating all combinations of priorities, which combinations are feasible,
    and if so, how many rounds can be achieved.

    Parameters
    -----
    num_teams: int, optional
        The number of teams
    """
    # 0. Construct Initial team_priority and priorities
    init_tp = {}
    priorities_for_team: dict[int, list[opb.OpposingTeams]] = {i: [] for i in range(1, num_teams)}
    for t in range(1, num_teams + 1):
        opposing_teams = [i for i in range(1, num_teams + 1) if t != i]
        init_tp[t] = tuple(opposing_teams)
        if t < num_teams:  # Fix the team_priority of the last team.
            for tp in itertools.permutations(opposing_teams):
                priorities_for_team[t].append(tp)

    # 1. Construuct Graph
    G = converter.convert_team_priority_to_graph(init_tp)

    # 2. Change some edges and test feasible
    cnt = 0
    cnt_feasible = 0
    old_comb = {init_tp[i]: i for i in range(1, num_teams)}
    for x in itertools.product(*priorities_for_team.values()):
        # [NOTE] mypy interprets x as `int`, but x is `Tuple[int, ...]`.
        new_comb = {ts: i for i, ts in enumerate(x, 1)}  # type: ignore

        # 2.1 Remove edge e (in old_comb \ new_comb)
        remove_diff = dict(old_comb.items() - new_comb.items())
        remove_priorities = {v: k for k, v in remove_diff.items()}
        remove_edges = converter.convert_team_priority_to_edges(remove_priorities)
        G.remove_edges_from(remove_edges)

        # 2.2 Add edge e (in new_comb \ old_comb)
        add_diff = dict(new_comb.items() - old_comb.items())
        add_priorities = {v: k for k, v in add_diff.items()}
        add_edges = converter.convert_team_priority_to_edges(add_priorities)
        G.add_edges_from(add_edges, color=opb.EDGE_COLOR)

        # 2.3 Test "Does the Graph G have topological sorted order ?"
        solver = opb.BaseProbSolverWithGraph.create_from_graph(num_teams, G)
        solver.solve()
        if solver.get_status() == opb.OPTIMAL:
            cnt_feasible += 1

        # 2.4 Update old_comb
        old_comb = new_comb
        cnt += 1

    # 3. Print answer
    print(f"{cnt = }, {cnt_feasible = }")


if __name__ == "__main__":
    experiment_all_combs_with_gurobi(num_teams=4, num_fixed=1)
    experiment_all_combs_with_graph_algorithm(num_teams=4)
