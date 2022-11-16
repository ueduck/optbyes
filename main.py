#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from optbyes import utils
from optbyes._typing import TeamPriority
from optbyes.optbyes import OptimizeNumberOfByes
from optbyes.problem.factory import BaseProblemFactory, MinimizeConsecutiveByesProblemFactory, ProblemFactory


def main(team_priority: TeamPriority, prob_type: str = "base") -> None:
    problem_factories = {"base": BaseProblemFactory(), "min_consec": MinimizeConsecutiveByesProblemFactory()}
    problem_factory: ProblemFactory = problem_factories[prob_type]
    ob = OptimizeNumberOfByes(team_priority, problem_factory)
    ob.solve()
    if ob.get_status() == OptimizeNumberOfByes.OPTIMAL:
        ob.print_schedule()


def check_all_combinations(num_teams: int = 4, num_fixed: int = 0) -> None:
    from scipy import special

    max_round = int(special.comb(num_teams, 2, exact=True))
    feasible_sols: dict[int, list[TeamPriority]] = {i: [] for i in range(num_teams - 1, max_round + 1)}
    team_priorities: list[TeamPriority] = utils.generate_team_priorities(num_teams, num_fixed)
    for tp in team_priorities:
        factory = BaseProblemFactory()
        ob = OptimizeNumberOfByes(tp, factory)
        ob.solve()
        if ob.get_status() == OptimizeNumberOfByes.OPTIMAL:
            feasible_sols[ob.get_num_rounds()].append(tp)

    all_combs = len(team_priorities)
    feasible_combs = sum(len(feasible_sols[i]) for i in range(num_teams - 1, max_round + 1))
    print(f"{all_combs = }, {feasible_combs = }")


if __name__ == "__main__":
    tp: TeamPriority = {1: (2, 3, 4), 2: (1, 4, 3), 3: (2, 1, 4), 4: (2, 3, 1)}
    main(tp, "base")
    check_all_combinations(num_teams=4, num_fixed=0)
