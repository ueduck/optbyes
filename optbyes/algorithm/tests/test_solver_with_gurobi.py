import pytest

import optbyes as opb


def test_not_runnnning_solve_method() -> None:
    tp: opb.TeamPriority = {1: (2, 3, 4), 2: (1, 3, 4), 3: (1, 4, 2), 4: (1, 2, 3)}
    factory = opb.BaseILPFactory()
    solver = opb.IterateNumRoundsAlgorithm.create_from_team_priority(tp, factory)
    with pytest.raises(opb.NotRunningSolveMethodError) as e:
        solver.get_schedule()
    assert str(e.value) == ""


def test_infeasible_instance() -> None:
    tp: opb.TeamPriority = {1: (2, 3, 4), 2: (1, 3, 4), 3: (1, 4, 2), 4: (1, 2, 3)}
    factory = opb.BaseILPFactory()
    solver = opb.IterateNumRoundsAlgorithm.create_from_team_priority(tp, factory)
    solver.solve()
    with pytest.raises(opb.InfeasibleInstanceError) as e:
        solver.get_schedule()
    assert str(e.value) == ""


def test_num_byes_teams4_byes8() -> None:
    tp: opb.TeamPriority = {1: (2, 3, 4), 2: (1, 3, 4), 3: (2, 1, 4), 4: (2, 3, 1)}
    factory = opb.BaseILPFactory()
    solver = opb.IterateNumRoundsAlgorithm.create_from_team_priority(tp, factory)
    solver.solve()
    num_byes = sum(solver.get_num_byes().values())
    assert num_byes == 8


def test_num_byes_teams4_byes12() -> None:
    tp1: opb.TeamPriority = {1: (2, 3, 4), 2: (1, 4, 3), 3: (2, 1, 4), 4: (2, 3, 1)}
    tp2: opb.TeamPriority = {1: (2, 3, 4), 2: (1, 4, 3), 3: (2, 1, 4), 4: (2, 1, 3)}
    for tp in [tp1, tp2]:
        factory = opb.BaseILPFactory()
        solver = opb.IterateNumRoundsAlgorithm.create_from_team_priority(tp, factory)
        solver.solve()
        num_byes = sum(solver.get_num_byes().values())
        assert num_byes == 12


def test_num_rounds_teams4_round3() -> None:
    team_priorities: list[opb.TeamPriority] = [
        {1: (2, 3, 4), 2: (1, 4, 3), 3: (4, 1, 2), 4: (3, 2, 1)},
        {1: (2, 4, 3), 2: (1, 3, 4), 3: (4, 2, 1), 4: (3, 1, 2)},
        {1: (3, 2, 4), 2: (4, 1, 3), 3: (1, 4, 2), 4: (2, 3, 1)},
        {1: (3, 4, 2), 2: (4, 3, 1), 3: (1, 2, 4), 4: (2, 1, 3)},
        {1: (4, 2, 3), 2: (3, 1, 4), 3: (2, 4, 1), 4: (1, 3, 2)},
        {1: (4, 3, 2), 2: (3, 4, 1), 3: (2, 1, 4), 4: (1, 2, 3)},
    ]
    for tp in team_priorities:
        factory = opb.BaseILPFactory()
        solver = opb.IterateNumRoundsAlgorithm.create_from_team_priority(tp, factory)
        solver.solve()
        assert solver.get_status() == opb.OPTIMAL
        assert solver.get_num_rounds() == 3


def test_num_rounds_teams4_round4() -> None:
    # {1: (2, 4, 3), 2: (1, 3, 4), 3: (4, 1, 2), 4: (3, 1, 2)} is round 5
    team_priorities: list[opb.TeamPriority] = [
        {1: (2, 3, 4), 2: (1, 3, 4), 3: (4, 1, 2), 4: (3, 1, 2)},
        {1: (2, 3, 4), 2: (1, 3, 4), 3: (4, 2, 1), 4: (3, 2, 1)},
        {1: (2, 3, 4), 2: (1, 4, 3), 3: (1, 2, 4), 4: (2, 1, 3)},
        {1: (2, 3, 4), 2: (1, 4, 3), 3: (1, 4, 2), 4: (2, 3, 1)},
        {1: (2, 3, 4), 2: (3, 1, 4), 3: (2, 4, 1), 4: (3, 2, 1)},
        {1: (2, 3, 4), 2: (4, 1, 3), 3: (4, 1, 2), 4: (2, 3, 1)},
    ]
    for tp in team_priorities:
        factory = opb.BaseILPFactory()
        prob = opb.IterateNumRoundsAlgorithm.create_from_team_priority(tp, factory)
        prob.solve()
        assert prob.get_status() == opb.OPTIMAL
        assert prob.get_num_rounds() == 4
