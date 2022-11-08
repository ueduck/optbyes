#! /usr/bin/env python3
# -*- coding: utf-8 -*-


from byesopt.optbyes import OptimizeByes
from byesopt.prob import BaseProblemFactory
from byesopt.utils import TeamSequence


def main() -> None:
    s: TeamSequence = {1: (2, 3, 4), 2: (1, 4, 3), 3: (2, 1, 4), 4: (2, 3, 1)}
    base_problem_factory = BaseProblemFactory()
    ob = OptimizeByes(s, base_problem_factory)
    ob.solve()
    if ob.get_status() == OptimizeByes.OPTIMAL:
        ob.print_schedule()


def check() -> None:
    import itertools

    num_teams = 4
    team_seqences = {i: [] for i in range(1, num_teams + 1)}
    for i in range(1, num_teams + 1):
        teams = [j for j in range(1, num_teams + 1) if i != j]
        for x in itertools.permutations(teams):
            team_seqences[i].append(x)

    cnt = 0
    cnt_feasible = 0
    for x in itertools.product(*team_seqences.values()):
        team_seqence = {i: s for i, s in enumerate(x, 1)}
        p = OptByes(team_seqence)
        p.solve()
        if p.getStatus() == OptByes.OPTIMAL:
            cnt_feasible += 1
        cnt += 1
    print(f"組合せ全体: {cnt}, 実行可能な組合せ: {cnt_feasible}")


if __name__ == "__main__":
    check()
    # main()
