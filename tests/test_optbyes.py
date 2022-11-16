from optbyes._typing import TeamPriority
from optbyes.optbyes import OptimizeNumberOfByes
from optbyes.problem.factory import BaseProblemFactory, ProblemFactory


def test_byes_teams4_round3() -> None:
    team_priorities: list[TeamPriority] = [
        {1: (2, 3, 4), 2: (1, 4, 3), 3: (4, 1, 2), 4: (3, 2, 1)},
        {1: (2, 4, 3), 2: (1, 3, 4), 3: (4, 2, 1), 4: (3, 1, 2)},
        {1: (3, 2, 4), 2: (4, 1, 3), 3: (1, 4, 2), 4: (2, 3, 1)},
        {1: (3, 4, 2), 2: (4, 3, 1), 3: (1, 2, 4), 4: (2, 1, 3)},
        {1: (4, 2, 3), 2: (3, 1, 4), 3: (2, 4, 1), 4: (1, 3, 2)},
        {1: (4, 3, 2), 2: (3, 4, 1), 3: (2, 1, 4), 4: (1, 2, 3)},
    ]
    for tp in team_priorities:
        factory: ProblemFactory = BaseProblemFactory()
        prob = OptimizeNumberOfByes(tp, factory)
        prob.solve()
        assert prob.get_status() == OptimizeNumberOfByes.OPTIMAL
        assert prob.get_num_rounds() == 3


def test_byes_teams4_round4() -> None:
    # {1: (2, 4, 3), 2: (1, 3, 4), 3: (4, 1, 2), 4: (3, 1, 2)} is round 5
    team_priorities: list[TeamPriority] = [
        {1: (2, 3, 4), 2: (1, 3, 4), 3: (4, 1, 2), 4: (3, 1, 2)},
        {1: (2, 3, 4), 2: (1, 3, 4), 3: (4, 2, 1), 4: (3, 2, 1)},
        {1: (2, 3, 4), 2: (1, 4, 3), 3: (1, 2, 4), 4: (2, 1, 3)},
        {1: (2, 3, 4), 2: (1, 4, 3), 3: (1, 4, 2), 4: (2, 3, 1)},
        {1: (2, 3, 4), 2: (3, 1, 4), 3: (2, 4, 1), 4: (3, 2, 1)},
        {1: (2, 3, 4), 2: (4, 1, 3), 3: (4, 1, 2), 4: (2, 3, 1)},
    ]
    for tp in team_priorities:
        factory: ProblemFactory = BaseProblemFactory()
        prob = OptimizeNumberOfByes(tp, factory)
        prob.solve()
        assert prob.get_status() == OptimizeNumberOfByes.OPTIMAL
        assert prob.get_num_rounds() == 4
