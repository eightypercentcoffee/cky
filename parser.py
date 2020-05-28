"""
CKY algorithm from the "Natural Language Processing" course by Michael Collins
https://class.coursera.org/nlangp-001/class
"""
import sys
from sys import stdin, stderr
from time import time
from json import dumps
from multiprocessing import Pool
import os

from collections import defaultdict
from pprint import pprint

from pcfg import PCFG
from tokenizer import PennTreebankTokenizer

def argmax(lst):
    return max(lst) if lst else (0.0, None)

def backtrace(back, bp):
    # ADD YOUR CODE HERE
    # Extract the tree from the backpointers

    if len(back) == 4:
        c, w, maxi, mini = back
        return [c, w]
    elif len(back) == 6:
        c, c1, c2, mini, mid, maxi = back
        backleft = bp[(mini, mid, c1)]
        backright = bp[(mid, maxi, c2)]
        return [c, backtrace(backleft, bp), backtrace(backright, bp)]

    # ADD YOUR CODE HERE
    # IMPLEMENT CKY

    # NOTE: norm_words is a list of pairs (norm, word), where word is the word 
    #       occurring in the input sentence and norm is either the same word, 
    #       if it is a known word according to the grammar, or the string _RARE_. 
    #       Thus, norm should be used for grammar lookup but word should be used 
    #       in the output tree.

    # Initialize your charts (for scores and backpointers)

    # Code for adding the words to the chart

    # Code for the dynamic programming part, where larger and larger subtrees are built

    # Below is one option for retrieving the best trees, assuming we only want trees with the "S" category
    # This is a simplification, since not all sentences are of the category "S"
    # The exact arguments also depends on how you implement your back-pointer chart.
    # Below it is also assumed that it is called "bp"
    # return backtrace(bp[0, n, "S"], bp) 

def CKY(pcfg, norm_words):
    chart = defaultdict(float)
    bp = defaultdict(tuple)

    for i in range(1, len(norm_words)+1):
        norm, word = norm_words[i-1]
        for key in pcfg.q1:
            rule, terminal = key
            if norm == terminal:
                chart[(i-1, i, rule)] = pcfg.q1[key]
                bp[(i-1, i, rule)] = (rule, word, i, i-1)
    for maximum in range(2, len(norm_words)+1):
        for minimum in range(maximum-2, -1, -1):
            for c in pcfg.binary_rules.keys():
                best = 0
                backpointer = None

                for children in pcfg.binary_rules[c]:
                    c1 = children[0]
                    c2 = children[1]

                    for mid in range(minimum+1, maximum):
                        if (minimum, mid, c1) in chart and (mid, maximum, c2) in chart:
                            t1 = chart[(minimum, mid, c1)]
                            t2 = chart[(mid, maximum, c2)]
                            candidate = t1 * t2 * pcfg.q2[(c, c1, c2)]

                            if candidate > best:
                                best = candidate
                                backpointer = (c, c1, c2, minimum, mid, maximum)
                if best > 0:
                    chart[(minimum, maximum, c)] = best
                    bp[(minimum, maximum, c)] = backpointer
    return backtrace(bp[0, len(norm_words), 'S'], bp)

        
class Parser:
    def __init__(self, pcfg):
        self.pcfg = pcfg
        self.tokenizer = PennTreebankTokenizer()
    
    def parse(self, sentence):
        words = self.tokenizer.tokenize(sentence)
        norm_words = []
        for word in words:                # rare words normalization + keep word
            norm_words.append((self.pcfg.norm_word(word), word))
        tree = CKY(self.pcfg, norm_words)
        tree[0] = tree[0].split("|")[0]
        return tree
    
def display_tree(tree):
    print(tree)

def multi_f(sentence):
    grammar_file = sys.argv[1]
    pcfg = PCFG()
    pcfg.load_model(grammar_file)
    parser = Parser(pcfg)
    tree = parser.parse(sentence)
    print(dumps(tree))

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("usage: python3 parser.py GRAMMAR")
        exit()

    start = time()
    grammar_file = sys.argv[1]
    print("Loading grammar from " + grammar_file + " ...", file=stderr)    
    pcfg = PCFG()
    pcfg.load_model(grammar_file)
    parser = Parser(pcfg)

    print("Parsing sentences ...", file=stderr)
    
    for sentence in stdin:
        tree = parser.parse(sentence)
        print(dumps(tree))

    print("Time: (%.2f)s\n" % (time() - start), file=stderr)
