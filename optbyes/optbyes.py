from scipy import special

from optbyes import utils
from optbyes._typing import Schedule, TeamPriority, TeamPriorityArray
from optbyes.exception import InfeasibleInstanceError, NotRunningSolveMethodError
from optbyes.problem.factory import ProblemFactory
from optbyes.problem.problem import Problem


class OptimizeNumberOfByes:
    CUTOFF_TIME = 600
    LOADED = Problem.LOADED
    OPTIMAL = Problem.OPTIMAL
    INFEASIBLE = Problem.INFEASIBLE

    def _get_team_priority_array(self, team_priority: TeamPriority) -> TeamPriorityArray:
        team_priority_array = utils.make_team_priority_array(team_priority)
        return team_priority_array

    def __init__(self, team_priority: TeamPriority, problem_factory: ProblemFactory) -> None:
        self._team_priority_array = self._get_team_priority_array(team_priority)
        self._num_teams = len(team_priority)
        self._num_rounds = self._num_teams - 1  # If the num of byes is 0, all games can be played in rounds of n - 1
        self._problem_factory = problem_factory
        self._optimal_state: Problem

    def solve(self) -> None:
        infeasible_flag = True
        max_round = int(special.comb(self._num_teams, 2, exact=True))
        while self._num_rounds <= max_round:
            print(f"\033[31m num_rounds = {self._num_rounds}\033[0m")
            p = self._problem_factory.create(self._num_teams, self._num_rounds, self._team_priority_array)
            self._status = self.LOADED
            p.solve()
            # Once the optimal solution is found,
            # the optimal schedule is saved and terminated.
            if p.get_status() == Problem.OPTIMAL:
                self._status = self.OPTIMAL
                self._optimal_state = p
                infeasible_flag = False
                break
            # If an optimal solution is not found,
            # increase the self._num_rounds.
            self._num_rounds += 1
            print("\n")
        # If self._num_rounds are increased up to 2n - 1 and the Problem is still infeasible,
        # it is considered to be INFEASIBLE.
        if infeasible_flag:
            self._status = self.INFEASIBLE

    def get_num_rounds(self) -> int:
        return self._num_rounds

    def get_status(self) -> int:
        return self._status

    def _check_status(self) -> None:
        if self._status == self.LOADED:
            raise NotRunningSolveMethodError("Execute the OptimizeByes.solve().")
        elif self._status == self.INFEASIBLE:
            raise InfeasibleInstanceError("Infeasible instance.")

    def get_schedule(self) -> Schedule:
        self._check_status()
        return self._optimal_state.get_schedule()

    def print_schedule(self) -> None:
        self._check_status()
        num_byes = self._optimal_state.get_num_byes()
        print(f"{num_byes = }")
        self._optimal_state.print_schedule()
