#!/usr/bin/bash

# Convert to cnf horizonal markovization second order, vertical full path

python3 cnf2.py < train.dat > train_cnf2.dat

python3 cnf2.py < dev.dat > dev_cnf2.dat

# Extract grammar

python3 pcfg.py train_cnf2.dat grammar2.dat

# CKY parsing with multiprocessing

python3 parser1.py grammar2.dat < dev.raw > dev_multi2.dat

# Evaluate parser

python3 eval.py dev_cnf2.dat dev_multi2.dat

# CKY parsing without multiprocessing

python3 parser.py grammar2.dat < dev.raw > dev_my2.dat

# Evaluate parser

python3 eval.py dev_cnf2.dat dev_my2.dat