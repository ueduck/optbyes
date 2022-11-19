from abc import ABCMeta, abstractmethod

from optbyes._typing import TeamPriorityArray
from optbyes.problem.problem import BaseProblem, MinimizeConsecutiveByesProblem, Problem


class ProblemFactory(metaclass=ABCMeta):
    @abstractmethod
    def create(self, num_teams: int, num_rounds: int, team_priority_array: TeamPriorityArray) -> Problem:
        raise NotImplementedError()


class BaseProblemFactory(ProblemFactory):
    def create(self, num_teams: int, num_rounds: int, team_priority_array: TeamPriorityArray) -> BaseProblem:
        return BaseProblem(num_teams, num_rounds, team_priority_array)


class MinimizeConsecutiveByesProblemFactory(ProblemFactory):
    def create(
        self, num_teams: int, num_rounds: int, team_priority_array: TeamPriorityArray
    ) -> MinimizeConsecutiveByesProblem:
        return MinimizeConsecutiveByesProblem(num_teams, num_rounds, team_priority_array)
