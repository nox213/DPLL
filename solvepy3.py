import argparse

class Variable:
        def __init__(self, value):
                self.value = value 

        def assign(self, value):
                self.value = value

class Literal:
        def __init__(self, variable, sign):
                self.variable = variable
                self.sign = sign

class Clause
        def __init__(self, literals):
                self.literals = literals
        def size(self):
                return len(self.literals)


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
                        for i in range(0, num_var):
                                variables.append(Variable(False))
                else:
                        numbers = line.split()
                        for number in numbers:
                                if int(number) == 0:
                                        break

                        
                        

        print(num_var)
        print(num_clause)
        print(is_cnf)
         

if __name__ == '__main__':
        main()

