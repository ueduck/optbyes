from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import final

import networkx as nx
from scipy import special

import optbyes as opb
from optbyes.utils import converter

__all__ = ["OptByesAlgorithm", "TopologicalSortAlgorithm", "IterateNumRoundsAlgorithm"]


class OptByesAlgorithm(metaclass=ABCMeta):
    """A base class for All related OptByes Algorithm

    This class is not usable as is, and should be subclassed to provide
    needed behavior.
    """

    COLOR_RED = "\033[31m"
    COLOR_NAN = "\033[0m"

    def __init__(self) -> None:
        self._status: opb.Status = opb.LOADED
        self._schedule: opb.Schedule = {}

    @abstractmethod
    def solve(self) -> None:
        raise NotImplementedError()

    @final
    def get_status(self) -> opb.Status:
        return self._status

    @final
    def get_schedule(self) -> opb.Schedule:
        if self._status != opb.OPTIMAL:
            raise opb.ERRORS[self._status]
        return self._schedule

    @final
    def print_schedule(self) -> None:
        schedule = self.get_schedule()

        team_1 = 1
        num_rounds = len(schedule[team_1])

        # print header
        print("r: ", end="")
        for r in range(1, num_rounds + 1):
            if r == num_rounds:
                print(r, end="")
                break
            print(r, end=" -> ")
        print()
        print("_____" * num_rounds)

        # print schedule for team_i
        for t, opposing_teams in schedule.items():
            print(f"{t}: ", end="")
            for round, team_j in opposing_teams.items():
                j = f"{self.COLOR_RED}b{self.COLOR_NAN}" if team_j == opb.BYES else team_j
                if round == num_rounds:
                    print(j, end="")
                    break
                print(j, end=" -> ")
            print()

    @final
    def get_num_byes(self) -> dict[int, int]:
        schedule = self.get_schedule()
        num_teams = len(schedule)
        num_byes = {t: 0 for t in range(1, num_teams + 1)}
        for t, opposing_teams in schedule.items():
            for team_j in opposing_teams.values():
                if team_j == opb.BYES:
                    num_byes[t] += 1
        return num_byes

    @final
    def get_num_rounds(self) -> int:
        schedule = self.get_schedule()
        teams_1 = 1
        num_rounds = len(schedule[teams_1])
        return num_rounds


class TopologicalSortAlgorithm(OptByesAlgorithm):
    """Solve the base problem using topological sort

    This algorithm solves the base problem using topological sort
    and check whether the instance is feasible or not,
    if so, how many rounds can be achieved.
    """

    def __init__(self) -> None:
        super().__init__()
        self._num_teams: int
        self._G: nx.DiGraph

    @classmethod
    def create_from_graph(cls, num_teams: int, G: nx.DiGraph) -> TopologicalSortAlgorithm:
        """Create instances of algorithm from directed graph

        Parameters
        -----
        num_teams: int
            The number of teams

        G: nx.DiGraph
            Graph experssing team priority

        Returns
        -----
        algorithm: TopologicalSortAlgorithm
            return this
        """
        algorithm = cls()
        algorithm._num_teams = num_teams
        algorithm._G = G.copy()
        return algorithm

    @classmethod
    def create_from_team_priority(cls, team_priority: opb.TeamPriority) -> TopologicalSortAlgorithm:
        """Create instances of algorithm from team_priority

        Parameters
        -----
        team_priority: opb.TeamPriority
            A dictionary of the team's desired priority order

        Returns
        -----
        algorithm: TopologicalSortAlgorithm
            return this
        """
        algorithm = cls()
        algorithm._num_teams = len(team_priority)
        G = converter.convert_team_priority_to_graph(team_priority)
        algorithm._G = G
        return algorithm

    def _is_feasible(self) -> bool:
        try:
            list(nx.topological_sort(self._G))
            return True
        except nx.NetworkXUnfeasible:
            return False

    def solve(self) -> None:
        if not (self._is_feasible()):
            self._status = opb.INFEASIBLE
            return

        self._status = opb.OPTIMAL
        self._schedule = {i: {} for i in range(1, self._num_teams + 1)}

        num_round = 1
        while len(self._G) != 0:
            for i in range(1, self._num_teams + 1):
                self._schedule[i][num_round] = opb.BYES  # initialize BYES
            for node, indegree in list(self._G.in_degree()):  # type: ignore
                if indegree != 0:
                    continue
                team_i, team_j = node  # node: opb.OpbNode = tuple[int, int]
                self._schedule[team_i][num_round] = team_j
                self._schedule[team_j][num_round] = team_i
                self._G.remove_node(node)
            num_round += 1


class IterateNumRoundsAlgorithm(OptByesAlgorithm):
    """Solve the base problem by iterating the number of rounds

    This algorithm solves the base problem by iterating the number of rounds,
    and check whether the instance is feasible or not,
    if so, how many rounds can be achieved.
    """

    def __init__(self) -> None:
        super().__init__()
        self._num_teams: int
        self._num_rounds: int
        self._tp_array: opb.TeamPriorityArray
        self._prob_factory: opb.ILPFactory

    @classmethod
    def create_from_team_priority(
        cls, team_priority: opb.TeamPriority, prob_factory: opb.ILPFactory
    ) -> IterateNumRoundsAlgorithm:
        """Create instances of algorithm from team_priority

        Parameters
        -----
        team_priority: opb.TeamPriority
            A dictionary of the team's desired priority order

        prob_factory: opb.ProblemFactory
            The type of integer programming model to create.
            The problem is dynamically generated as it is solved multiple times
            while changing the number of rounds.

        Returns
        -----
        algorithm: IterateNumRoundsAlgorithm
            return this
        """
        algorithm = cls()
        algorithm._num_teams = len(team_priority)
        algorithm._num_rounds = len(team_priority) - 1
        tp_array = converter.convert_team_priority_to_team_priority_array(team_priority)
        algorithm._tp_array = tp_array
        algorithm._prob_factory = prob_factory
        return algorithm

    def solve(self) -> None:
        infeasible_flag = True
        max_round = int(special.comb(self._num_teams, 2, exact=True))
        while self._num_rounds <= max_round:
            print(f"{self.COLOR_RED}num_rounds = {self._num_rounds}{self.COLOR_NAN}")
            prob = self._prob_factory.create(self._num_teams, self._num_rounds, self._tp_array)
            prob.solve()
            # Once the optimal solution is found,
            # the optimal schedule is saved and terminated.
            if prob.get_status() == opb.OPTIMAL:
                self._status = opb.OPTIMAL
                self._schedule = prob.get_schedule()
                infeasible_flag = False
                break
            # If an optimal solution is not found,
            # increase the self._num_rounds.
            self._num_rounds += 1
        # If self._num_rounds are increased up to 2n - 1 and the Problem is still infeasible,
        # it is considered to be INFEASIBLE.
        if infeasible_flag:
            self._status = opb.INFEASIBLE
