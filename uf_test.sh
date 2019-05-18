#!/bin/bash

for f in ./input/*.cnf; do python3 solvepy3.py $f; done

