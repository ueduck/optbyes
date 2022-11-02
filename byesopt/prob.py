import gurobipy as gp


class Prob:
    CUTOFF_TIME = 600

    def __init__(self, num_teams: int, num_rounds: int, team_sequences: dict[int, tuple[int, int, int]]) -> None:
        self._num_teams = num_teams
        self._num_rounds = num_rounds
        self._team_sequences = self._makeSequence(team_sequences)
        self._model = gp.Model("ByesModel")
        self._xvar: dict[tuple[int, int, int], gp.Var] = {}
        self._yvar: dict[tuple[int, int], gp.Var] = {}

    @staticmethod
    def _makeSequence(team_sequences: dict[int, tuple[int, int, int]]) -> dict[tuple[int, int, int], int]:
        s_ijk = {}
        # 先行順序が必要なところだけ1を埋める
        for team_k, seq in team_sequences.items():
            for i in range(len(seq) - 1):
                team_i = seq[i]
                for j in range(i + 1, len(seq)):
                    team_j = seq[j]
                    s_ijk[team_k, team_i, team_j] = 1

        # 先行順序が定まっていなければ0を埋める(Model内でのKeyError対策)
        for t in team_sequences.keys():
            for i in team_sequences.keys():
                for j in team_sequences.keys():
                    try:
                        s_ijk[t, i, j]
                    except KeyError:
                        s_ijk[t, i, j] = 0
        return s_ijk

    def solve(self) -> None:
        self._createVariables()
        self._createConstraintFunctions()
        self._createObjectiveFunction()
        self._model.setParam("TimeLimit", self.CUTOFF_TIME)
        self._model.update()
        self._model.optimize()

    def _createVariables(self) -> None:
        for i in range(1, self._num_teams + 1):
            for j in range(1, self._num_teams + 1):
                for r in range(1, self._num_rounds + 1):
                    self._xvar[i, j, r] = self._model.addVar(vtype="B", name=f"x_{i}_{j}_{r}")

        for i in range(1, self._num_teams + 1):
            for r in range(1, self._num_rounds + 1):
                self._yvar[i, r] = self._model.addVar(vtype="B", name=f"y_{i}_{r}")

    def _createConstraintFunctions(self) -> None:
        # 1, 2
        for r in range(1, self._num_rounds + 1):
            for i in range(1, self._num_teams + 1):
                for j in range(1, self._num_teams + 1):
                    if i == j:
                        self._model.addConstr(self._xvar[i, j, r] == 0)
                    self._model.addConstr(self._xvar[i, j, r] == self._xvar[j, i, r])

        # 3
        for i in range(1, self._num_teams + 1):
            for j in range(1, self._num_teams + 1):
                if i != j:
                    c3 = gp.quicksum(self._xvar[i, j, r] for r in range(1, self._num_rounds + 1))
                    self._model.addConstr(c3 == 1)

        # 4
        for r in range(1, self._num_rounds + 1):
            for i in range(1, self._num_teams + 1):
                c4 = gp.quicksum(self._xvar[i, j, r] for j in range(1, self._num_teams + 1))
                self._model.addConstr(1 - c4 == self._yvar[i, r])

        # 5
        for i in range(1, self._num_teams + 1):
            for k in range(1, self._num_teams + 1):
                for j in range(1, self._num_teams + 1):
                    for r in range(2, self._num_rounds + 1):
                        c51 = self._team_sequences[k, i, j] * gp.quicksum(self._xvar[k, i, rp] for rp in range(1, r))
                        c52 = self._team_sequences[k, i, j] * self._xvar[k, j, r]
                        self._model.addConstr(c51 >= c52)

        # 6
        for k in range(1, self._num_teams + 1):
            for j in range(1, self._num_teams + 1):
                c61 = self._num_teams * (1 - self._xvar[k, j, 1])
                c62 = gp.quicksum(self._team_sequences[k, i, j] for i in range(1, self._num_teams + 1))
                self._model.addConstr(c61 >= c62)

        # 7
        for r in range(1, self._num_rounds + 1):
            for i in range(1, self._num_teams + 1):
                c6 = gp.quicksum(self._xvar[i, j, r] for j in range(1, self._num_teams + 1))
                self._model.addConstr(c6 <= 1)

    def _createObjectiveFunction(self) -> None:
        obj = gp.quicksum(
            self._yvar[i, r] for i in range(1, self._num_teams + 1) for r in range(1, self._num_rounds + 1)
        )
        self._model.setObjective(obj, gp.GRB.MINIMIZE)

    def getNumByes(self) -> int:
        num_byes = 0
        for i in range(1, self._num_teams + 1):
            for r in range(1, self._num_rounds + 1):
                if self._yvar[i, r].X == 1:
                    num_byes += 1
        return num_byes

    def getMipGap(self) -> float:
        return self._model.MIPGap

    def getStatus(self) -> int:
        return self._model.Status

    def getSchedule(self) -> dict[int, dict[int, str]]:
        teams = {}
        for i in range(1, self._num_teams + 1):
            team_i = {}
            for r in range(1, self._num_rounds + 1):
                if self._yvar[i, r].X == 1:
                    team_i[r] = "b"
                for j in range(1, self._num_teams + 1):
                    if self._xvar[i, j, r].X == 1:
                        team_i[r] = f"{j}"
            teams[i] = team_i
        return teams

    def printSchedule(self) -> None:
        print("r: ", end="")
        for r in range(1, self._num_rounds + 1):
            if r == self._num_rounds:
                print(r, end="")
                break
            print(r, end=" -> ")
        print()
        print("_____" * self._num_rounds)

        solution = self.getSchedule()
        for i, seq in solution.items():
            print(f"{i}: ", end="")
            for r, j in seq.items():
                if j == "b":
                    j = "\033[31mb\033[0m"
                if r == self._num_rounds:
                    print(j, end="")
                    break
                print(j, end=" -> ")
            print()
