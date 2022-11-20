from abc import ABCMeta, abstractmethod
from typing import final

import gurobipy as gp

import optbyes as opb

__all__ = [
    "ILP",
    "BaseILP",
]


class ILP(metaclass=ABCMeta):
    """A base class for Problem.

    This class is not usable as is, and should be subclassed to provide
    needed behavior.

    Parameters
    -----
    num_teams: int
        The number of teams

    num_rounds: int
        The number of round ( >= num_teams - 1)

    team_priority_array: opb.TeamPriorityArray
        Parameters such that 1 if team k plays team i before team j
        (team_priority_array[k, i, j] = 1), 0 otherwise.
    """

    def __init__(self, num_teams: int, num_rounds: int, team_priority_array: opb.TeamPriorityArray) -> None:
        self._num_teams = num_teams
        self._num_rounds = num_rounds
        self._tp_array = team_priority_array
        self._status: int = opb.LOADED
        self._schedule: opb.Schedule = {}

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
    def _optimize(self) -> None:
        raise NotImplementedError()

    @final
    def solve(self) -> None:
        self._create_variables()
        self._create_constraint_functions()
        self._create_objective_function()
        self._optimize()

    @final
    def get_status(self) -> int:
        return self._status

    @final
    def get_schedule(self) -> opb.Schedule:
        if self._status != opb.OPTIMAL:
            raise opb.ERRORS[self._status]
        return self._schedule


class BaseILP(ILP):
    """Modeler and Solver for Base Byes Problem

    Solve with the Base Byes problem by Gurobi,
    under the condition that num_rounds = R

    Parameters
    -----
    num_teams: int
        The number of teams

    num_rounds: int
        The number of round ( >= num_teams - 1)

    team_priority_array: opb.TeamPriorityArray
        Parameters such that 1 if team k plays team i before team j
        (team_priority_array[k, i, j] = 1), 0 otherwise.
    """

    NAME = "BaseILP"

    def __init__(self, num_teams: int, num_rounds: int, team_priority_array: opb.TeamPriorityArray) -> None:
        super().__init__(num_teams, num_rounds, team_priority_array)
        self._model = gp.Model(self.NAME)
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
        self._constraint_function_1()
        self._constraint_function_2()
        self._constraint_function_3()
        self._constraint_function_4()
        self._constraint_function_5()
        self._constraint_function_6()

    def _constraint_function_1(self) -> None:
        for r in range(1, self._num_rounds + 1):
            for i in range(1, self._num_teams + 1):
                for j in range(1, self._num_teams + 1):
                    if i == j:
                        self._model.addConstr(self._xvar[i, j, r] == 0)
                    self._model.addConstr(self._xvar[i, j, r] == self._xvar[j, i, r])

    def _constraint_function_2(self) -> None:
        for i in range(1, self._num_teams + 1):
            for j in range(1, self._num_teams + 1):
                if i != j:
                    c = gp.quicksum(self._xvar[i, j, r] for r in range(1, self._num_rounds + 1))
                    self._model.addConstr(c == 1)

    def _constraint_function_3(self) -> None:
        for r in range(1, self._num_rounds + 1):
            for i in range(1, self._num_teams + 1):
                c = gp.quicksum(self._xvar[i, j, r] for j in range(1, self._num_teams + 1))
                self._model.addConstr(1 - c == self._yvar[i, r])

    def _constraint_function_4(self) -> None:
        for i in range(1, self._num_teams + 1):
            for k in range(1, self._num_teams + 1):
                for j in range(1, self._num_teams + 1):
                    for r in range(2, self._num_rounds + 1):
                        c1 = self._tp_array[k, i, j] * gp.quicksum(self._xvar[k, i, x] for x in range(1, r))
                        c2 = self._tp_array[k, i, j] * self._xvar[k, j, r]
                        self._model.addConstr(c1 >= c2)

    def _constraint_function_5(self) -> None:
        for k in range(1, self._num_teams + 1):
            for j in range(1, self._num_teams + 1):
                c1 = self._num_teams * (1 - self._xvar[k, j, 1])
                c2 = gp.quicksum(self._tp_array[k, i, j] for i in range(1, self._num_teams + 1))
                self._model.addConstr(c1 >= c2)

    def _constraint_function_6(self) -> None:
        for r in range(1, self._num_rounds + 1):
            for i in range(1, self._num_teams + 1):
                c = gp.quicksum(self._xvar[i, j, r] for j in range(1, self._num_teams + 1))
                self._model.addConstr(c <= 1)

    def _create_objective_function(self) -> None:
        obj = gp.quicksum(
            self._yvar[i, r] for i in range(1, self._num_teams + 1) for r in range(1, self._num_rounds + 1)
        )
        self._model.setObjective(obj, gp.GRB.MINIMIZE)

    def _optimize(self) -> None:
        self._model.optimize()

        # set status
        if self._model.Status != gp.GRB.OPTIMAL:
            self._status = opb.INFEASIBLE
            return

        # create schedule
        self._status = opb.OPTIMAL
        for i in range(1, self._num_teams + 1):
            team_i = {}
            for r in range(1, self._num_rounds + 1):
                if self._yvar[i, r].X == 1:
                    team_i[r] = opb.BYES
                for j in range(1, self._num_teams + 1):
                    if self._xvar[i, j, r].X == 1:
                        team_i[r] = j
            self._schedule[i] = team_i
