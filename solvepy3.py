import argparse

class Variable:
        def __init__(self, assign):
                self.assign = assign 
        def __hash__(self):
                return hash(self.assign)
        def __eq__(self, other):
                if self.assign == other.assign:
                        return True
                else:
                        return False

class Literal:
        def __init__(self, variable, sign):
                self.variable = variable
                self.sign = sign
        def __hash__(self):
                return hash((self.variable, self.sign))
        def __eq__(self, other):
                if self.variable == other.variable and self.sign == other.sign:
                        return True
                else:
                        return False
        def evaluate(self):
                if self.sign == True:
                        return self.variable.assign
                else:
                        return not self.variable.assign
                       
#def dpll(clauses, partial_assignment):
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
                                variables.append(Variable(False))
                else:
                        numbers = line.split()
                        literals = []
                        for number in numbers:
                                n = int(number)
                                sign = True
                                if n == 0:
                                        break
                                if n < 0:
                                        sign = False
                                literals.append(Literal(variables[n], sign))
                                temp = frozenset(literals)
                                clauses.add(temp)

#      dpll(clauses, variables)
#    print(num_var)
#        print(num_clause)
#        print(is_cnf)
         

if __name__ == '__main__':
        main()

