#!/bin/bash

for f in ./cbs/*.cnf; do python3 solvepy3.py $f; done

