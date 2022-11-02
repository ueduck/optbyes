import gurobipy as gp

from .exception import InfeasibleInstanceError, NotRunningSolveMethodError
from .prob import Prob


class OptByes:
    LOAD = 1
    OPTIMAL = 2
    INFEASIBLE = 3

    def __init__(self, team_sequences: dict[int, tuple[int, int, int]]) -> None:
        self._team_sequences = team_sequences
        self._num_teams = len(team_sequences)
        self._num_rounds = len(team_sequences) - 1
        self._status = self.LOAD
        self._optimal_state: Prob

    def solve(self) -> None:
        infeasible_flag = True
        while self._num_rounds <= 2 * self._num_teams - 1:
            print(f"\033[31m num_rounds = {self._num_rounds}\033[0m")
            p = Prob(self._num_teams, self._num_rounds, self._team_sequences)
            p.solve()
            # 最適解が見つかればそれを出力して終了
            if p.getStatus() == gp.GRB.OPTIMAL:
                self._status = self.OPTIMAL
                print(self._status)
                self._optimal_state = p
                infeasible_flag = False
                break
            # そうでなければラウンドの数を増やす
            self._num_rounds += 1
            print("\n")
        # 2n - 1までラウンドを増やして実行不能の場合は実行不能判定
        if infeasible_flag:
            self._status = self.INFEASIBLE

    def getStatus(self) -> int:
        return self._status

    def getSchedule(self) -> dict[int, dict[int, str]]:
        self._checkStatus()
        return self._optimal_state.getSchedule()

    def printSchedule(self) -> None:
        self._checkStatus()
        num_byes = self._optimal_state.getNumByes()
        print(f"{num_byes = }")
        self._optimal_state.printSchedule()

    def _checkStatus(self) -> None:
        print(f"xx{self._status}")
        if self._status == self.LOAD:
            raise NotRunningSolveMethodError("solveメソッドを実行してください")
        elif self._status == self.INFEASIBLE:
            raise InfeasibleInstanceError("実行不可能なインスタンスです")
