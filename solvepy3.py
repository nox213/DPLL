import argparse
from copy import deepcopy

def find_unit_clause(clauses, variables):
        f_a = deepcopy(clauses)
        unit_clause = -1
        empty_clause = -1
        i = 0
        for clause in f_a:
                for literal in clause:
                        value = variables[abs(literal)]
                        if literal > 0:
                                sign = 1
                        else:
                                sign = -1
                        if value == -1:
                                continue
                        if value * sign == 1:
                                f_a.remove(clause)
                        else:
                                clause.remove(literal)
                                if len(clause) == 0:
                                        empty_clause = i
                                elif len(clause) == 1
                                        unit_clause = i
                i += 1
                                
        return f_a, unit_clause, empty_clause

def resolve(c1, c2, p)
        if p in c1:
                resolvent = (c1 - set(p)) | (c2 - set([-p]))
        else:
                resolvent = (c1 - set(-p)) | (c2 - set([p]))

        return resolvent

def clause_learning(clauses, decision, empty_clause):
        conflict = clauses[empty_clause]
        for d in reversed(decision):
                if d[2] == True || d[0] not in conflict:
                        continue
                else:
                        conflict = resolvent(conflict, d[3], d[0])
        return conflict

def dpll(clauses, variables):
        clauses_l = list(clauses)
        is_unsat = False
        decision = []

        #unit propagation
        while True:
                while True:
                        f_a, unit_clause, empty_clause = find_unit_clause(clauses, variables)
                        if len(f_a) == 0
                                return decision
                        elif empty_clause >= 0:
                                break
                        elif unit_clause >= 0:
                                c = clauses_l[unit_clause]
                                l = list(c)[0]
                                #(literal, value, decision, C_i)
                                if l > 0:
                                        decision.append((l, 1, False, unit_clause)        
                                        variables[abs(l)] = 1
                                else:
                                        decision.append((l, 0, False, unit_clause)        
                                        variables[abs(l)] = 0
                        else:
                                break

                if empty_clause >= 0:
                        learned_clause = clause_learning(clauses_l, decision, empty_clause)
                        if len(learned_clause) == 0:
                                is_unsat = True
                                break
                        clauses.add(learned_clause)
                else:
                        decision.append

        if is_unsat == True
                print('s UNSATISFIABLE')
        else:
                print('s SATISFIABLE')
                for i in range(len(decision)):


                                

def main():
        parser = argparse.ArgumentParser()
        parser.add_argument("file", help="input for dpll")
        args = parser.parse_args()
        print(args.file)

        variables = []
        clauses = set()
        
        f = open(args.file, 'r')
        lines = f.readlines()
        for line in lines:
                if line[0] == 'c':
                        continue
                elif line[0] == 'p':
                        param = line.split()
                        if param[1] == 'cnf':
                                is_cnf = True
                        else:
                                is_cnf = False
                        num_var = int(param[2])
                        num_clause = int(param[3])
                        for i in range(0, num_var + 1):
                                variables.append(-1)
                else:
                        numbers = line.split()
                        literals = []
                        for number in numbers:
                                n = int(number)
                                if n == 0:
                                        break
                                literals.append(n)
                                temp = frozenset(literals)
                                clauses.add(temp)

#      dpll(clauses, variables)
#    print(num_var)
#        print(num_clause)
#        print(is_cnf)
         

if __name__ == '__main__':
        main()

