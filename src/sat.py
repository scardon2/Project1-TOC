"""
SAT Solver - DIMACS-like Multi-instance Format
----------------------------------------------------------
Project 1: Tough Problems & The Wonderful World of NP

INPUT FORMAT (multi-instance file):
-----------------------------------
Each instance starts with a comment and a problem definition:

c <instance_id> <k> <status?>
p cnf <n_vertices> <n_edges>
u,v
x,y
...

Example:
c 1 3 ?
p cnf 4 5
1,2
1,3
2,3
2,4
3,4
c 2 2 ?
p cnf 3 3
1,2
2,3
1,3

OUTPUT:
-------
A CSV file named 'resultsfile.csv' with columns:
instance_id,n_vars,n_clauses,method,satisfiable,time_seconds,solution


EXAMPLE OUTPUT
------------
instance_id,n_vars,n_clauses,method,satisfiable,time_seconds,solution
3,4,10,U,0.00024808302987366915,BruteForce,{}
4,4,10,S,0.00013304100139066577,BruteForce,"{1: True, 2: False, 3: False, 4: False}"
"""

from typing import List, Tuple, Dict
from src.helpers.sat_solver_helper import SatSolverAbstractClass
import itertools


class SatSolver(SatSolverAbstractClass):

    """
        NOTE: The output of the CSV file should be same as EXAMPLE OUTPUT above otherwise you will loose marks
        For this you dont need to save anything just make sure to return exact related output.
        
        For ease look at the Abstract Solver class and basically we are having the run method which does the saving
        of the CSV file just focus on the logic
    """
    ###### HELPERS !!!!!!!
    #########

    def literal_true(self, lit: int, A: Dict[int, bool]) -> bool:
        # check if a literaleral is satisfied under A
        # when lit > 0, variable must be true
        # when lit < 0, variable must be false

        v = abs(lit)
        val = A.get(v, None) # none = unassigned
        if val is None:
            return False
        return (lit > 0 and val) or (lit < 0 and not val)

    def clause_satisfied(self, clause: List[int], A: Dict[int, bool]) -> bool:
        # the clause is satisfied when at least one literal is true

        for lit in clause:
            if self.literal_true(lit, A):
                return True
        return False

    def clause_impossible(self, clause: List[int], A: Dict[int, bool]) -> bool:
        # clause becomes impossible if:
        # #  none of the assigned literals make it true AND
        # #  there are no unassigned literals left that could change hthe outcome

        has_unassigned = False
        for lit in clause:
            v = abs(lit)
            if v not in A:
                has_unassigned = True
            elif self.literal_true(lit, A):
                return False
        return not has_unassigned

    #########
    ##### END OF HELPERS !!!!!

    def sat_backtracking(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        # builds partial assignment and prunes when a clause becomes unsatisfiable

        A: Dict[int, bool] = {} # partial assignment
        solved_model: Dict[int, bool] = {}

        def tri_state() -> str:
            # check of partial assignment:
            #   "yes" -> all clauses satisfied
            #   "no" -> at least one clause already impossible
            #   "maybe" -> otherwise keep going

            all_true = True
            for c in clauses:
                if self.clause_satisfied(c, A):
                    continue
                # not yet satisfied
                all_true = False
                if self.clause_impossible(c, A):
                    return "no"
            return "yes" if all_true else "maybe"

        def pick_unassigned() -> int:
            # return next unassigned variable 

            for v in range(1, n_vars+1):
                if v not in A:
                    return v
            return 0

        def dfs() -> bool:
            nonlocal solved_model

            state = tri_state()
            if state == "yes":
                solved_model = A.copy()
                return True
            if state == "no":
                return False

            v = pick_unassigned()
            if v == 0:
                return False

            # try true then false
            A[v] = True
            if dfs():
                return True
            A[v] = False
            if dfs():
                return True
            
            # backtrack
            del A[v]
            return False

        if dfs():
            return True, solved_model

        return False, {}

    def sat_bruteforce(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        # iterate over all bit-vectors of length n_vars 
        # tries every assignment of n_vars

        for bits in itertools.product([False, True], repeat=n_vars):
            # build assignment dict for bit-vectors
            A = {i+1: bits[i] for i in range(n_vars)}
            ok = True
            for c in clauses:
                if not self.clause_satisfied(c, A):
                    ok = False
                    break
            if ok:
                return True, A

        return False, {}

    def sat_bestcase(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        pass

    def sat_simple(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        pass