#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import gurobipy as gp

from byesopt.prob import Prob


def test_byes_teams4_rounds5() -> None:
    s = {1: (2, 3, 4), 2: (1, 3, 4), 3: (2, 1, 4), 4: (2, 3, 1)}
    num_teams = 4
    num_rounds_1 = 4
    num_rounds_2 = 5
    p1 = Prob(num_teams, num_rounds_1, s)
    p2 = Prob(num_teams, num_rounds_2, s)
    p1.solve()
    p2.solve()
    assert p1.getStatus() == gp.GRB.INFEASIBLE
    assert p2.getStatus() == gp.GRB.OPTIMAL
    assert p2.getNumByes() == 8


def test_byes_teams4_rounds6_1() -> None:
    s = {1: (2, 3, 4), 2: (1, 4, 3), 3: (2, 1, 4), 4: (2, 3, 1)}
    num_teams = len(s.keys())
    num_rounds_1 = 5
    num_rounds_2 = 6
    p1 = Prob(num_teams, num_rounds_1, s)
    p2 = Prob(num_teams, num_rounds_2, s)
    p1.solve()
    p2.solve()
    assert p1.getStatus() == gp.GRB.INFEASIBLE
    assert p2.getStatus() == gp.GRB.OPTIMAL
    assert p2.getNumByes() == 12


def test_byes_teams4_rounds6_2() -> None:
    s = {1: (2, 3, 4), 2: (1, 4, 3), 3: (2, 1, 4), 4: (2, 1, 3)}
    num_teams = len(s.keys())
    num_rounds_1 = 5
    num_rounds_2 = 6
    p1 = Prob(num_teams, num_rounds_1, s)
    p2 = Prob(num_teams, num_rounds_2, s)
    p1.solve()
    p2.solve()
    assert p1.getStatus() == gp.GRB.INFEASIBLE
    assert p2.getStatus() == gp.GRB.OPTIMAL
    assert p2.getNumByes() == 12
