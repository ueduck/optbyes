OpposingTeams = tuple[int, ...]
TeamPriority = dict[int, OpposingTeams]

Status = int
Schedule = dict[int, dict[int, int]]

# Integer Programming Model
TeamPriorityArray = dict[tuple[int, int, int], int]

# Graph
OpbNode = tuple[int, int]
OpbEdge = tuple[OpbNode, OpbNode]
Coordinate = tuple[float, float]
Pos = dict[OpbNode, Coordinate]
