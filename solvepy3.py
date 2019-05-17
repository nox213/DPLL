import argparse
from copy import deepcopy

def find_unit_clause(clauses, variables):
        f_a = deepcopy(clauses)
        unit_clause = -1
        empty_clause = -1
        for i, clause in list(enumerate(clauses)):
                for literal in clause:
                        value = variables[abs(literal)]
                        if value == -1:
                                continue
                        if literal > 0:
                                sign = 1
                        else:
                                sign = -1
                        idx = i - (len(clauses) - len(f_a))
                        if (value == 1 and sign == 1) or (value == 0 and sign == -1):
                                f_a.pop(idx)
                                break
                        else:
                                f_a[idx] -= set([literal])
                                if len(f_a[idx]) == 0:
                                        empty_clause = i

        for i, clause in list(enumerate(f_a)):
                if len(clause) == 1:
                        unit_clause = i
                        break

        return f_a, unit_clause, empty_clause

def resolve(c1, c2, p):
        if p in c1:
                resolvent = (c1 - set([p])) | (c2 - set([-p]))
        else:
                resolvent = (c1 - set([-p])) | (c2 - set([p]))

        return resolvent

def clause_learning(clauses, decision, empty_clause, variables):
        conflict = clauses[empty_clause]
        for d in reversed(decision):
                if (d[2] == True) or (d[0] not in conflict):
                        continue
                else:
                        conflict = resolve(conflict, clauses[d[3]], d[0])
        variables[decision.pop()[0]] = -1
        while True:
                is_unit = True
                for d in decision:
                        if d[0] in conflict or -d[0] in conflict:
                                is_unit = False
                                break
                if is_unit == True:
                        break
                variables[decision.pop()[0]] = -1
                        
        return conflict

def decise_variable(clauses, variables, decision):
        i = 0
        for variable in variables:
                if variable == -1:
                        return i
                i += 1
                
def dpll(clauses, variables, decision):
        #unit propagation
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
                        p_a = dpll(clauses, variables, decision + [((var, 1, False, unit_clause))])
                        variables[abs(l)] = 0
                else:
                        variables[abs(l)] = 0
                        p_a = dpll(clauses, variables, decision + [((var, 0, False, unit_clause))])
                        variables[abs(l)] = 1

                if len(p_a) > 0:
                        return p_a
                else:
                        return list()
        else:
                break

        if empty_clause >= 0:
                learned_clause = clause_learning(clauses, decision, empty_clause, variables)
                clauses.append(learned_clause)
                if len(learned_clause) == 0:
                        return list()

        var = decise_variable(clauses, variables, decision)
        variables[var] = 1
        p_a = dpll(clauses, variables, decision + [((var, 1, True))])
        if len(p_a) > 0:
                return p_a
        variables[var] = 0
        p_a = dpll(clauses, variables, decision + [((var, 0, True))])
        variables[var] = -1
        return p_a

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
        p_a = dpll(list(clauses), variables, list())
        if len(p_a) > 0:
                print('s SATISFIABLE')
        else:
                print('s SATISFIABLE')

if __name__ == '__main__':
        main()
