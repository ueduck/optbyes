from abc import ABCMeta, abstractmethod

import gurobipy as gp
from typing_extensions import final

from optbyes._typing import Schedule, TeamPriorityArray
from optbyes.exception import InfeasibleInstanceError, NotRunningSolveMethodError


class Problem(metaclass=ABCMeta):
    LOADED = 1
    OPTIMAL = 2
    INFEASIBLE = 3
    BYES = "b"

    def __init__(self, num_teams: int, num_rounds: int, team_priority_array: TeamPriorityArray) -> None:
        self._num_teams = num_teams
        self._num_rounds = num_rounds
        self._team_priority_array = team_priority_array
        self._status: int = self.LOADED

    @abstractmethod
    def _create_variables(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _create_constraint_functions(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _create_objective_function(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _optimize(self, cutoff_time: float) -> None:
        raise NotImplementedError()

    @final
    def solve(self, cutoff_time: float = 3600) -> None:
        self._create_variables()
        self._create_constraint_functions()
        self._create_objective_function()
        self._optimize(cutoff_time)

    @final
    def get_status(self) -> int:
        return self._status

    @final
    def _check_status(self) -> None:
        if self._status == self.OPTIMAL:
            return
        if self._status == self.LOADED:
            raise NotRunningSolveMethodError("Execute the OptimizeByes.solve().")
        if self._status == self.INFEASIBLE:
            raise InfeasibleInstanceError("Infeasible instance.")
        raise Exception(f"Status: {self._status = }")

    @abstractmethod
    def get_schedule(self) -> Schedule:
        raise NotImplementedError()

    @final
    def get_num_byes(self) -> int:
        schedule = self.get_schedule()
        cnt_byes = 0
        for i in range(1, self._num_teams + 1):
            for r in range(1, self._num_rounds + 1):
                if schedule[i][r] == self.BYES:
                    cnt_byes += 1
        return cnt_byes

    @final
    def print_schedule(self) -> None:
        self._check_status()
        print("r: ", end="")
        for r in range(1, self._num_rounds + 1):
            if r == self._num_rounds:
                print(r, end="")
                break
            print(r, end=" -> ")
        print()
        print("_____" * self._num_rounds)

        solution = self.get_schedule()
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


class BaseProblem(Problem):
    MODEL_NAME = "BaseModel"

    def __init__(self, num_teams: int, num_rounds: int, team_priority_array: TeamPriorityArray) -> None:
        super().__init__(num_teams, num_rounds, team_priority_array)
        self._model = gp.Model(self.MODEL_NAME)
        self._xvar: dict[tuple[int, int, int], gp.Var] = {}
        self._yvar: dict[tuple[int, int], gp.Var] = {}

    def _create_variables(self) -> None:
        for i in range(1, self._num_teams + 1):
            for j in range(1, self._num_teams + 1):
                for r in range(1, self._num_rounds + 1):
                    self._xvar[i, j, r] = self._model.addVar(vtype="B", name=f"x_{i}_{j}_{r}")

        for i in range(1, self._num_teams + 1):
            for r in range(1, self._num_rounds + 1):
                self._yvar[i, r] = self._model.addVar(vtype="B", name=f"y_{i}_{r}")

    def _create_constraint_functions(self) -> None:
        # (1-1), (1-2)
        for r in range(1, self._num_rounds + 1):
            for i in range(1, self._num_teams + 1):
                for j in range(1, self._num_teams + 1):
                    if i == j:
                        self._model.addConstr(self._xvar[i, j, r] == 0)
                    self._model.addConstr(self._xvar[i, j, r] == self._xvar[j, i, r])

        # (2)
        for i in range(1, self._num_teams + 1):
            for j in range(1, self._num_teams + 1):
                if i != j:
                    c = gp.quicksum(self._xvar[i, j, r] for r in range(1, self._num_rounds + 1))
                    self._model.addConstr(c == 1)

        # (3)
        for r in range(1, self._num_rounds + 1):
            for i in range(1, self._num_teams + 1):
                c = gp.quicksum(self._xvar[i, j, r] for j in range(1, self._num_teams + 1))
                self._model.addConstr(1 - c == self._yvar[i, r])

        # (4)
        for i in range(1, self._num_teams + 1):
            for k in range(1, self._num_teams + 1):
                for j in range(1, self._num_teams + 1):
                    for r in range(2, self._num_rounds + 1):
                        c1 = self._team_priority_array[k, i, j] * gp.quicksum(self._xvar[k, i, x] for x in range(1, r))
                        c2 = self._team_priority_array[k, i, j] * self._xvar[k, j, r]
                        self._model.addConstr(c1 >= c2)

        # (5)
        for k in range(1, self._num_teams + 1):
            for j in range(1, self._num_teams + 1):
                c1 = self._num_teams * (1 - self._xvar[k, j, 1])
                c2 = gp.quicksum(self._team_priority_array[k, i, j] for i in range(1, self._num_teams + 1))
                self._model.addConstr(c1 >= c2)

        # (6)
        for r in range(1, self._num_rounds + 1):
            for i in range(1, self._num_teams + 1):
                c = gp.quicksum(self._xvar[i, j, r] for j in range(1, self._num_teams + 1))
                self._model.addConstr(c <= 1)

    def _create_objective_function(self) -> None:
        obj = gp.quicksum(
            self._yvar[i, r] for i in range(1, self._num_teams + 1) for r in range(1, self._num_rounds + 1)
        )
        self._model.setObjective(obj, gp.GRB.MINIMIZE)

    def _optimize(self, cutoff_time: float) -> None:
        self._model.setParam("TimeLimit", cutoff_time)
        self._model.optimize()
        self._status = self._model.Status

    def get_schedule(self) -> Schedule:
        self._check_status()
        teams: Schedule = {}
        for i in range(1, self._num_teams + 1):
            team_i = {}
            for r in range(1, self._num_rounds + 1):
                if self._yvar[i, r].X == 1:
                    team_i[r] = self.BYES
                for j in range(1, self._num_teams + 1):
                    if self._xvar[i, j, r].X == 1:
                        team_i[r] = str(j)
            teams[i] = team_i
        return teams


class MinimizeConsecutiveByesProblem(BaseProblem):
    MODEL_NAME = "MinimizeConsecutiveByesModel"

    def __init__(self, num_teams: int, num_rounds: int, team_priority_array: TeamPriorityArray) -> None:
        super().__init__(num_teams, num_rounds, team_priority_array)
        self._model = gp.Model(self.MODEL_NAME)
        self._mvar: dict[tuple[int, int], gp.Var] = {}

    def _create_variables(self) -> None:
        super()._create_variables()
        for i in range(1, self._num_teams + 1):
            for r in range(2, self._num_rounds + 1):
                self._mvar[i, r] = self._model.addVar(vtype="B", name=f"m_{i}_{r}")

    def _create_constraint_functions(self) -> None:
        super()._create_constraint_functions()

        # (7)
        for i in range(1, self._num_teams + 1):
            for r in range(2, self._num_rounds + 1):
                self._model.addConstr(self._yvar[i, r - 1] <= self._mvar[i, r] + self._yvar[i, r])

    def _create_objective_function(self) -> None:
        obj = gp.quicksum(
            self._mvar[i, r] for i in range(1, self._num_teams + 1) for r in range(2, self._num_rounds + 1)
        )
        self._model.setObjective(obj, gp.GRB.MAXIMIZE)
