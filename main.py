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


if __name__ == "__main__":
    main()
