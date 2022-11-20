#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import time

import optbyes as opb
from optbyes.utils import converter


def main(team_priority: opb.TeamPriority) -> None:
    # solve Graph
    solver_graph = opb.BaseProbSolverWithGraph.create_from_team_priority(team_priority)
    # solve ILP
    factory = opb.BaseILPFactory()
    solver_ilp = opb.ProbSolverWithGurobi.create_from_team_priority(team_priority, factory)

    # Graph Algorithm vs Gurobi
    calc_times: dict[str, float] = {}
    solvers: dict[str, opb.OptByesSolver] = {"graph": solver_graph, "gurobi": solver_ilp}
    for solver_name, solver in solvers.items():
        start_time = time.perf_counter()
        solver.solve()
        calc_time = time.perf_counter() - start_time
        calc_times[solver_name] = calc_time
        if solver.get_status() == opb.OPTIMAL:
            solver.print_schedule()
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
