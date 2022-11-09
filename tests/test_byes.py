#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from optbyes.optbyes import OptimizeByes
from optbyes.problem import BaseProblem, Problem
from optbyes.utils import TeamSequence


def test_byes_teams4_rounds5() -> None:
    s: TeamSequence = {1: (2, 3, 4), 2: (1, 3, 4), 3: (2, 1, 4), 4: (2, 3, 1)}
    s_array = OptimizeByes.make_team_sequence_array(s)
    num_teams = 4
    num_rounds_1 = 4
    num_rounds_2 = 5
    p1 = BaseProblem(num_teams, num_rounds_1, s_array)
    p2 = BaseProblem(num_teams, num_rounds_2, s_array)
    p1.solve()
    p2.solve()
    assert p1.get_status() == Problem.INFEASIBLE
    assert p2.get_status() == Problem.OPTIMAL
    assert p2.get_num_byes() == 8


def test_byes_teams4_rounds6_1() -> None:
    s: TeamSequence = {1: (2, 3, 4), 2: (1, 4, 3), 3: (2, 1, 4), 4: (2, 3, 1)}
    s_array = OptimizeByes.make_team_sequence_array(s)
    num_teams = len(s.keys())
    num_rounds_1 = 5
    num_rounds_2 = 6
    p1 = BaseProblem(num_teams, num_rounds_1, s_array)
    p2 = BaseProblem(num_teams, num_rounds_2, s_array)
    p1.solve()
    p2.solve()
    assert p1.get_status() == Problem.INFEASIBLE
    assert p2.get_status() == Problem.OPTIMAL
    assert p2.get_num_byes() == 12


def test_byes_teams4_rounds6_2() -> None:
    s: TeamSequence = {1: (2, 3, 4), 2: (1, 4, 3), 3: (2, 1, 4), 4: (2, 1, 3)}
    s_array = OptimizeByes.make_team_sequence_array(s)
    num_teams = len(s.keys())
    num_rounds_1 = 5
    num_rounds_2 = 6
    p1 = BaseProblem(num_teams, num_rounds_1, s_array)
    p2 = BaseProblem(num_teams, num_rounds_2, s_array)
    p1.solve()
    p2.solve()
    assert p1.get_status() == Problem.INFEASIBLE
    assert p2.get_status() == Problem.OPTIMAL
    assert p2.get_num_byes() == 12
