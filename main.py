#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import time

import optbyes as opb
from optbyes.utils import converter


def main(team_priority: opb.TeamPriority) -> None:
    # solve with Graph
    algorithm_1 = opb.TopologicalSortAlgorithm.create_from_team_priority(team_priority)
    # solve with ILP
    factory = opb.BaseILPFactory()
    algorithm_2 = opb.IterateNumRoundsAlgorithm.create_from_team_priority(team_priority, factory)

    # Graph Algorithm vs Gurobi
    calc_times: dict[str, float] = {}
    algorithms: dict[str, opb.OptByesAlgorithm] = {"graph": algorithm_1, "gurobi": algorithm_2}
    for algorithm_name, algorithm in algorithms.items():
        start_time = time.perf_counter()
        algorithm.solve()
        calc_time = time.perf_counter() - start_time
        calc_times[algorithm_name] = calc_time
        if algorithm.get_status() == opb.OPTIMAL:
            algorithm.print_schedule()
    print(calc_times)

    # Draw graph and simulate schedule
    G = converter.convert_team_priority_to_graph(team_priority)
    opb.draw_simulation("./figures/sample.gif", G, interval=1200)


if __name__ == "__main__":
    # feasible instance
    tp1: opb.TeamPriority = {1: (2, 3, 4), 2: (1, 3, 4), 3: (1, 2, 4), 4: (1, 2, 3)}
    # infeasible instance
    tp2: opb.TeamPriority = {1: (2, 3, 4), 2: (1, 3, 4), 3: (1, 4, 2), 4: (1, 2, 3)}
    main(tp1)
