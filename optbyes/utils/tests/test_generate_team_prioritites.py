from optbyes.utils import generator


def test_teams4() -> None:
    num_teams = 4
    num_tps = {0: 1296, 1: 216, 2: 36, 3: 6, 4: 1}
    for i in range(num_teams + 1):
        tps = generator.generate_team_priorities(num_teams, i)
        assert len(tps) == num_tps[i]
