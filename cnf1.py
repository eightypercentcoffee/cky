from sys import stdin, stderr
from json import loads, dumps

def cnf(tree):
    if len(tree) == 2 and isinstance(tree[0], str) and isinstance(tree[1], str):
        return tree
    elif len(tree) <= 2:
        return cnf([tree[0]+'+'+tree[1][0]] + tree[1][1:])
    elif len(tree) == 3:
        return [tree[0], cnf(tree[1]), cnf(tree[2])]
    elif len(tree) > 3:
        return [tree[0], cnf(tree[1]), cnf([tree[0].split('|')[0]+'|'+tree[1][0]] + tree[2:])]
        # return [tree[0], cnf(tree[1]), cnf([tree[0]+'|'+tree[1][0]] + tree[2:])]


def is_cnf(tree):
    n = len(tree)
    if n == 2:
        return isinstance(tree[1], str)
    elif n == 3:
        return is_cnf(tree[1]) and is_cnf(tree[2])
    else:
        return False

def words(tree):
    if isinstance(tree, str):
        return [tree]
    else:
        ws = []
        for t in tree[1:]:
            ws = ws + words(t)
        return ws

if __name__ == "__main__":

    #print('CNF conversion using:\nHorizontal: first order\nVertical: full path', file=stderr)
    #print('', file=stderr)

    for line in stdin:
        tree = loads(line)
        sentence = words(tree)
        input = str(dumps(tree))
        cnf(tree)
        tree = cnf(tree)
        if is_cnf(tree) and words(tree) == sentence:
            print(dumps(tree))
        else:
            print("Something went wrong!", file=stderr)
            print("Sentence: " + " ".join(sentence), file=stderr)
            print("Input: " + input, file=stderr)
            print("Output: " + str(dumps(tree)), file=stderr)
            exit()
