from abc import ABCMeta, abstractmethod

import optbyes as opb

__all__ = [
    "ILPFactory",
    "BaseILPFactory",
]


class ILPFactory(metaclass=ABCMeta):
    @abstractmethod
    def create(self, num_teams: int, num_rounds: int, tp_array: opb.TeamPriorityArray) -> opb.ILP:
        raise NotImplementedError()


class BaseILPFactory(ILPFactory):
    def create(self, num_teams: int, num_rounds: int, tp_array: opb.TeamPriorityArray) -> opb.BaseILP:
        return opb.BaseILP(num_teams, num_rounds, tp_array)
