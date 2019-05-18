#!/bin/bash

for f in ./input2/*.cnf; do python3 solvepy3.py $f; done

