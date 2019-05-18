import argparse
import random
from copy import deepcopy

def find_unit_clause(clauses, variables):
        f_a = deepcopy(clauses)
        unit_list = []
        empty_list = []
        true_list = []
        for i, clause in list(enumerate(clauses)):
                for literal in clause:
                        value = variables[abs(literal)]
                        if value == -1:
                                if len(f_a[i]) == 1:
                                        unit_list.append(i)
                                continue
                        if literal > 0:
                                sign = 1
                        else:
                                sign = -1
                        if (value == 1 and sign == 1) or (value == 0 and sign == -1):
                                true_list.append(i)
                                break
                        else:
                                f_a[i] -= set([literal])
                                if len(f_a[i]) == 0:
                                        empty_list.append(i)
                                if len(f_a[i]) == 1:
                                        unit_list.append(i)
        
        for empty in empty_list:
                if empty in unit_list:
                        unit_list.remove(empty)
        for true in true_list:
                if true in unit_list:
                        unit_list.remove(true)
        unit_clause = -1
        empty_clause = -1
        if len(empty_list) > 0:
                empty_clause = empty_list.pop()
        if len(unit_list) > 0:
                unit_clause = unit_list.pop()
        if len(true_list) == len(clauses):
                f_a = []

        return f_a, unit_clause, empty_clause

def resolve(c1, c2, p):
        if p in c1:
                resolvent = (c1 - set([p])) | (c2 - set([-p]))
        else:
                resolvent = (c1 - set([-p])) | (c2 - set([p]))

        return resolvent

def clause_learning(clauses, decision, empty_clause, variables):
#        print('decision')
#        print(decision)
        conflict = clauses[empty_clause]
#        print('C')
#        print(conflict)
        for d in reversed(decision):
                if (d[2] == True) or ((d[0] not in conflict) and (-d[0] not in conflict)):
                        continue
                else:
                        conflict = resolve(conflict, clauses[d[3]], d[0])
#        print('learned clause')
#        print(conflict)
        while True:
                is_unit = True
                for d in decision:
                        if d[0] in conflict or -d[0] in conflict:
                                is_unit = False
                                break
                if is_unit == True:
                        break
                variables[decision.pop()[0]] = -1
                        
#        print('backtrcked')
#        print(decision)
        return conflict

def decise_variable(clauses, variables, decision):
        i = 0
        for variable in variables:
                if variable == -1:
                        return i
                i += 1
                
def dpll(clauses, variables):
        decision = []
        #unit propagation
        while True:
                while True:
                        f_a, unit_clause, empty_clause = find_unit_clause(clauses, variables)
                        if len(f_a) == 0:
                                return decision
                        elif empty_clause >= 0:
                                break
                        elif unit_clause >= 0:
                                c = f_a[unit_clause]
                                l = list(c)[0]
                                #(variable, value, decision, C_i)
                                if l > 0:
                                        variables[abs(l)] = 1
                                        decision.append((abs(l), 1, False, unit_clause))
                                else:
                                        variables[abs(l)] = 0
                                        decision.append((abs(l), 0, False, unit_clause))
                        else:
                                break

                if empty_clause >= 0:
                        learned_clause = clause_learning(clauses, decision, empty_clause, variables)
                        clauses.append(learned_clause)
#   for i in range(80, len(clauses)):
#                                print(clauses[i])
#                        print('==========================')
                        if len(learned_clause) == 0:
                                return list()
                else:
                        var = decise_variable(clauses, variables, decision)
                        variables[var] = 1
                        decision.append((var, 1, True))
#decision.append((var, random.randrange(0,2), True))

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

        #variable 0 is not used
        variables[0] = 100
        p_a = dpll(list(clauses), variables)
        if len(p_a) > 0:
                print('s SATISFIABLE')
        else:
                print('s SATISFIABLE')

if __name__ == '__main__':
        main()
