#!/bin/bash

for f in *.cnf; do python3 solvepy3.py $f; done

