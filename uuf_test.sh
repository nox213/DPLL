#!/bin/bash

for f in ./uuf/UUF50.218.1000/*.cnf; do python3 solvepy3.py $f; done

