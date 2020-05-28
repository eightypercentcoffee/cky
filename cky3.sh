#!/usr/bin/bash

# Convert to cnf horizonal markovization ∞, vertical full path

python3 cnf3.py < train.dat > train_cnf3.dat

python3 cnf3.py < dev.dat > dev_cnf3.dat

# Extract grammar

python3 pcfg.py train_cnf3.dat grammar3.dat

# CKY parsing with multiprocessing

python3 parser1.py grammar3.dat < dev.raw > dev_multi3.dat

# Evaluate parser

python3 eval.py dev_cnf3.dat dev_multi3.dat

# CKY parsing without multiprocessing

python3 parser.py grammar3.dat < dev.raw > dev_my3.dat

# Evaluate parser

python3 eval.py dev_cnf3.dat dev_my3.dat