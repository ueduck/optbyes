from optbyes._typing import TeamPriority, TeamPriorityArray


def make_team_priority_array(team_priority: TeamPriority) -> TeamPriorityArray:
    team_priority_array: TeamPriorityArray = {}
    # for team k, team i -> team j => sequence[k, i, j] = 1
    for team_k, seq in team_priority.items():
        for i in range(len(seq) - 1):
            team_i = seq[i]
            for j in range(i + 1, len(seq)):
                team_j = seq[j]
                team_priority_array[team_k, team_i, team_j] = 1
    # otherwise
    for t in team_priority.keys():
        for i in team_priority.keys():
            for j in team_priority.keys():
                try:
                    team_priority_array[t, i, j]
                except KeyError:
                    team_priority_array[t, i, j] = 0
    return team_priority_array
