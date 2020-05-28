#!/usr/bin/bash

# Convert to cnf horizonal markovization first order, vertical full path

python3 cnf1.py < train.dat > train_cnf1.dat

python3 cnf1.py < dev.dat > dev_cnf1.dat

# Extract grammar

python3 pcfg.py train_cnf1.dat grammar1.dat

# CKY parsing with multiprocessing

python3 parser1.py grammar1.dat < dev.raw > dev_multi1.dat

# Evaluate parser

python3 eval.py dev_cnf1.dat dev_multi1.dat

# CKY parsing without multiprocessing

python3 parser.py grammar1.dat < dev.raw > dev_my1.dat

# Evaluate parser

python3 eval.py dev_cnf1.dat dev_my1.dat