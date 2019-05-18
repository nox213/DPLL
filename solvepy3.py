import argparse
import random
from copy import deepcopy

def find_unit_clause(clauses, variables, vars_freq):
        f_a = deepcopy(clauses)
        unit_clauses = []
        empty_clauses = []
        true_clauses = []

        for var in vars_freq:
                var[1] = 0
                var[2] = 0
                var[3] = 0

        for i, clause in list(enumerate(clauses)):
                for literal in clause:
                        vars_freq[abs(literal)][1] += 1
                        value = variables[abs(literal)]
                        if value == -1:
                                if len(f_a[i]) == 1:
                                        unit_clauses.append(i)
                                continue
                        if literal > 0:
                                sign = 1
                                vars_freq[abs(literal)][2] += 1
                        else:
                                sign = -1
                                vars_freq[abs(literal)][3] += 1
                        if (value == 1 and sign == 1) or (value == 0 and sign == -1):
                                true_clauses.append(i)
                                break
                        else:
                                f_a[i] -= set([literal])
                                vars_freq[abs(literal)][1] -= 1
                                if sign == 1:
                                        vars_freq[abs(literal)][2] -= 1
                                else:
                                        vars_freq[abs(literal)][3] -= 1
                                if len(f_a[i]) == 0:
                                        empty_clauses.append(i)
                                if len(f_a[i]) == 1:
                                        unit_clauses.append(i)
        
        for empty in empty_clauses:
                if empty in unit_clauses:
                        unit_clauses.remove(empty)
        for true in true_clauses:
                if true in unit_clauses:
                        unit_clauses.remove(true)
        unit_clause = -1
        empty_clause = -1
        if len(empty_clauses) > 0:
                empty_clause = empty_clauses.pop()
        if len(unit_clauses) > 0:
                unit_clause = unit_clauses.pop()
        if len(true_clauses) == len(clauses):
                f_a = []

        return f_a, unit_clause, empty_clause, true_clauses

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

def decise_variable(clauses, variables, decision, variables_freq):
        variables_freq.sort(reverse=True, key=lambda frequency: frequency[1])
        for variable in variables_freq:
                var = variable[0]
                if var != 0 and variables[var] == -1:
                        return var

def min_conflict(var, f_a, true_clauses):

        true = 0
        false = 0
        for i, clause in list(enumerate(f_a)):
                if i in true_clauses:
                        continue
                if var in clause:
                        true += 1
                elif -var in clause:
                        false += 1

        if true > false:
                return 1
        else:
                return 0

                
def dpll(clauses, variables, vars_freq):
        decision = []
        learned = []
        #unit propagation
        while True:
                while True:
#print(decision)
                        f_a, unit_clause, empty_clause, true_clauses = find_unit_clause(clauses, variables, vars_freq)
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
                        if learned_clause in learned:
                                print('duplicate!!')
                                return list()
                        learned.append(learned_clause)
                        if len(learned_clause) == 0:
                                return list()
                else:
                        var = decise_variable(clauses, variables, decision, vars_freq)
                        variables[var] = 1
                        value = min_conflict(var, f_a, true_clauses)
                        decision.append((var, value, True))
#decision.append((var, random.randrange(0,2), True))

def main():
        parser = argparse.ArgumentParser()
        parser.add_argument("file", help="input for dpll")
        args = parser.parse_args()
        print(args.file)

        variables = []
        vars_freq = []
        clauses = set()
        
        f = open(args.file, 'r')
        lines = f.readlines()
        for line in lines:
                if line[0] == 'c' or line[0] == '%' or line[0] == '0':
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
                                vars_freq.append([i, 0, 0, 0])
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
        p_a = dpll(list(clauses), variables, vars_freq)
        if len(p_a) > 0:
                print('s SATISFIABLE')
        else:
                print('s UNSATISFIABLE')

if __name__ == '__main__':
        main()
