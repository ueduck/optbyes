import optbyes as opb
from optbyes.utils import converter


def test_base_ilp_teams4_rounds5() -> None:
    tp: opb.TeamPriority = {1: (2, 3, 4), 2: (1, 3, 4), 3: (2, 1, 4), 4: (2, 3, 1)}
    tp_array = converter.convert_team_priority_to_team_priority_array(tp)
    num_teams = 4
    num_rounds_1 = 4
    num_rounds_2 = 5
    prob1 = opb.BaseILP(num_teams, num_rounds_1, tp_array)
    prob2 = opb.BaseILP(num_teams, num_rounds_2, tp_array)
    prob1.solve()
    prob2.solve()
    assert prob1.get_status() == opb.INFEASIBLE
    assert prob2.get_status() == opb.OPTIMAL


def test_base_ilp_teams4_rounds6_1() -> None:
    tp: opb.TeamPriority = {1: (2, 3, 4), 2: (1, 4, 3), 3: (2, 1, 4), 4: (2, 3, 1)}
    tp_array = converter.convert_team_priority_to_team_priority_array(tp)
    num_teams = 4
    num_rounds_1 = 5
    num_rounds_2 = 6
    prob1 = opb.BaseILP(num_teams, num_rounds_1, tp_array)
    prob2 = opb.BaseILP(num_teams, num_rounds_2, tp_array)
    prob1.solve()
    prob2.solve()
    assert prob1.get_status() == opb.INFEASIBLE
    assert prob2.get_status() == opb.OPTIMAL


def test_base_problem_teams4_rounds6_2() -> None:
    tp: opb.TeamPriority = {1: (2, 3, 4), 2: (1, 4, 3), 3: (2, 1, 4), 4: (2, 1, 3)}
    tp_array = converter.convert_team_priority_to_team_priority_array(tp)
    num_teams = 4
    num_rounds_1 = 5
    num_rounds_2 = 6
    prob1 = opb.BaseILP(num_teams, num_rounds_1, tp_array)
    prob2 = opb.BaseILP(num_teams, num_rounds_2, tp_array)
    prob1.solve()
    prob2.solve()
    assert prob1.get_status() == opb.INFEASIBLE
    assert prob2.get_status() == opb.OPTIMAL
