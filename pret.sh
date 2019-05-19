#!/bin/bash

for f in ./pret/*.cnf; do python3 solvepy3.py $f; done

