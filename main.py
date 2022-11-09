#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from optbyes.optbyes import OptimizeByes
from optbyes.problem import BaseProblemFactory, MinimizeConsecutiveByesProblemFactory, ProblemFactory
from optbyes.utils import TeamSequence


def main(prob_type: str = "base") -> None:
    s: TeamSequence = {1: (2, 3, 4), 2: (1, 4, 3), 3: (2, 1, 4), 4: (2, 3, 1)}
    factories = {"base": BaseProblemFactory(), "min_consec": MinimizeConsecutiveByesProblemFactory()}
    factory: ProblemFactory = factories[prob_type]
    ob = OptimizeByes(s, factory)
    ob.solve()
    if ob.get_status() == OptimizeByes.OPTIMAL:
        ob.print_schedule()


def check_all_combinations(num_teams: int = 4) -> None:
    import itertools

    team_seqences: dict[int, list[tuple[int, ...]]] = {i: [] for i in range(1, num_teams + 1)}
    for i in range(1, num_teams + 1):
        teams = [j for j in range(1, num_teams + 1) if i != j]
        for x in itertools.permutations(teams):
            team_seqences[i].append(x)

    cnt = 0
    cnt_feasible = 0
    opt_rounds = {i: 0 for i in range(num_teams - 1, 2 * num_teams)}
    opt_rounds_seqences = {i: [] for i in range(num_teams - 1, 2 * num_teams)}
    for x in itertools.product(*(team_seqences.values())):
        # [NOTE] Type check of mypy is wrong.
        team_seqence: TeamSequence = {i: s for i, s in enumerate(x, 1)}  # type: ignore
        factory = BaseProblemFactory()
        ob = OptimizeByes(team_seqence, factory)
        ob.solve()
        if ob.get_status() == OptimizeByes.OPTIMAL:
            opt_rounds[ob.get_num_rounds()] += 1
            opt_rounds_seqences[ob.get_num_rounds()].append(team_seqence)
            cnt_feasible += 1
        cnt += 1
    print(f"組合せ全体: {cnt}, 実行可能な組合せ: {cnt_feasible}")
    print(f"{opt_rounds = }")
    num_rounds = num_teams - 1
    print(f"{opt_rounds_seqences[num_rounds]}")


if __name__ == "__main__":
    main("base")
    check_all_combinations(num_teams=4)
