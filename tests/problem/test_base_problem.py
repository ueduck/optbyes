from optbyes import utils
from optbyes._typing import TeamPriority
from optbyes.problem.problem import BaseProblem, Problem


def test_base_problem_teams4_rounds5() -> None:
    tp: TeamPriority = {1: (2, 3, 4), 2: (1, 3, 4), 3: (2, 1, 4), 4: (2, 3, 1)}
    tp_array = utils.make_team_priority_array(tp)
    num_teams = 4
    num_rounds_1 = 4
    num_rounds_2 = 5
    prob1 = BaseProblem(num_teams, num_rounds_1, tp_array)
    prob2 = BaseProblem(num_teams, num_rounds_2, tp_array)
    prob1.solve()
    prob2.solve()
    assert prob1.get_status() == Problem.INFEASIBLE
    assert prob2.get_status() == Problem.OPTIMAL
    assert prob2.get_num_byes() == 8


def test_base_problem_teams4_rounds6_1() -> None:
    tp: TeamPriority = {1: (2, 3, 4), 2: (1, 4, 3), 3: (2, 1, 4), 4: (2, 3, 1)}
    tp_array = utils.make_team_priority_array(tp)
    num_teams = 4
    num_rounds_1 = 5
    num_rounds_2 = 6
    prob1 = BaseProblem(num_teams, num_rounds_1, tp_array)
    prob2 = BaseProblem(num_teams, num_rounds_2, tp_array)
    prob1.solve()
    prob2.solve()
    assert prob1.get_status() == Problem.INFEASIBLE
    assert prob2.get_status() == Problem.OPTIMAL
    assert prob2.get_num_byes() == 12


def test_base_problem_teams4_rounds6_2() -> None:
    tp: TeamPriority = {1: (2, 3, 4), 2: (1, 4, 3), 3: (2, 1, 4), 4: (2, 1, 3)}
    tp_array = utils.make_team_priority_array(tp)
    num_teams = 4
    num_rounds_1 = 5
    num_rounds_2 = 6
    prob1 = BaseProblem(num_teams, num_rounds_1, tp_array)
    prob2 = BaseProblem(num_teams, num_rounds_2, tp_array)
    prob1.solve()
    prob2.solve()
    assert prob1.get_status() == Problem.INFEASIBLE
    assert prob2.get_status() == Problem.OPTIMAL
    assert prob2.get_num_byes() == 12
