import optbyes as opb


class NotRunningSolveMethodError(Exception):
    """Execute the OptimizeByes.solve()."""


class InfeasibleInstanceError(Exception):
    """Infeasible instance."""


ERRORS = {
    opb.LOADED: NotRunningSolveMethodError(),
    opb.INFEASIBLE: InfeasibleInstanceError(),
}
