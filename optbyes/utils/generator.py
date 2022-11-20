import itertools

import optbyes as opb

__all__ = [
    "generate_team_priorities",
]


def generate_team_priorities(num_teams: int, num_fixed: int = 0) -> list[opb.TeamPriority]:
    """Generate a set of team priority combinations.

    Parameters
    -----
    num_teams: int
        The number of teams
    num_fixed: int, optional (default = 0)
        The number of teams to fix priorities. Defaults to 0.

    Returns
    -----
    team_priorities: list[opb.TeamPriority]
        A dictionary of the team's desired priority order

    Examples
    -----
    >>> generate_team_priorities(4, 4)
    >>> [{1: (2, 3, 4), 2: (1, 3, 4), 3: (1, 2, 4), 4: (1, 2, 3)}]
    >>> generate_team_priorities(3)
    >>> [
            {1: (2, 3), 2: (1, 3), 3: (1, 2)}, {1: (2, 3), 2: (1, 3), 3: (2, 1)},
            {1: (2, 3), 2: (3, 1), 3: (1, 2)}, {1: (2, 3), 2: (3, 1), 3: (1, 2)},
            {1: (3, 2), 2: (1, 3), 3: (1, 2)}, {1: (3, 2), 2: (1, 3), 3: (2, 1)},
            {1: (3, 2), 2: (3, 1), 3: (1, 2)}, {1: (3, 2), 2: (3, 1), 3: (2, 1)},
        ]
    """
    if num_fixed > num_teams:
        raise ValueError("num_fixed must be less than num_teams.")

    # Fix the priority of the teams i (1 <= i <= num_fixed).
    fixed_team_priorities = {}
    for i in range(1, num_fixed + 1):
        fixed_team_priorities_for_team_i = [t for t in range(1, num_teams + 1) if t != i]
        fixed_team_priorities[i] = tuple(fixed_team_priorities_for_team_i)

    # ex) priorities_for_team = {1: [(2, 3, 4), (2, 4, 3), ...], 2: [...]}
    priorities_for_team: dict[int, list[opb.OpposingTeams]] = {i: [] for i in range(num_fixed + 1, num_teams + 1)}
    for i in range(num_fixed + 1, num_teams + 1):
        opposing_teams = [t for t in range(1, num_teams + 1) if t != i]
        for x in itertools.permutations(opposing_teams):
            priorities_for_team[i].append(x)

    team_priorities: list[opb.TeamPriority] = []  # ex) [{1: (2, 3, 4), 2: (1, 3, 4), ...}, {...}]
    for x in itertools.product(*(priorities_for_team.values())):
        team_priority: opb.TeamPriority = {}
        # fixed priority teams
        for i in range(1, num_fixed + 1):
            team_priority[i] = fixed_team_priorities[i]
        # flexible priority teams
        for i, s in enumerate(x, num_fixed + 1):
            team_priority[i] = s  # type: ignore
        team_priorities.append(team_priority)
    return team_priorities
