from .exception import InfeasibleInstanceError, NotRunningSolveMethodError
from .problem import Problem, ProblemFactory
from .utils import Schedule, TeamSequence, TeamSequenceArray


class OptimizeByes:
    CUTOFF_TIME = 600
    LOADED = Problem.LOADED
    OPTIMAL = Problem.OPTIMAL
    INFEASIBLE = Problem.INFEASIBLE

    def __init__(self, team_sequence: TeamSequence, problem_factory: ProblemFactory) -> None:
        self._num_teams = len(team_sequence)
        self._num_rounds = len(team_sequence) - 1
        self._team_sequence_array = self.make_team_sequence_array(team_sequence)
        self._problem_factory = problem_factory
        self._optimal_state: Problem

    @staticmethod
    def make_team_sequence_array(team_sequence: TeamSequence) -> TeamSequenceArray:
        sequence_array = {}
        # for team k, team i -> team j => sequence[k, i, j] = 1
        for team_k, seq in team_sequence.items():
            for i in range(len(seq) - 1):
                team_i = seq[i]
                for j in range(i + 1, len(seq)):
                    team_j = seq[j]
                    sequence_array[team_k, team_i, team_j] = 1
        # otherwise
        for t in team_sequence.keys():
            for i in team_sequence.keys():
                for j in team_sequence.keys():
                    try:
                        sequence_array[t, i, j]
                    except KeyError:
                        sequence_array[t, i, j] = 0
        return sequence_array

    def solve(self) -> None:
        infeasible_flag = True
        while self._num_rounds <= 2 * self._num_teams - 1:
            print(f"\033[31m num_rounds = {self._num_rounds}\033[0m")
            p = self._problem_factory.create(self._num_teams, self._num_rounds, self._team_sequence_array)
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
