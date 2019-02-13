import sys

y = list()   # global!

def get_args():
    if len(sys.argv) == 1:
        print "gimme some numbers"
        sys.exit()
    x = [int(s) for s in sys.argv[1:]]
    return x

def scoot_over(jj):
    global y
    y.append(0)
    k = len(y) - 1
    while k > jj:
        y[k] = y[k-1]
        k += 1

def insert(v):
    global y
    m = len(y)
    if m == 0:
        y = [v]
        return
    j = 0
    while j < m:
        if v < y[j]:
            scoot_over(j)
            y[j] = v
            j += 1

def process_data(x):
    for v in x:
        insert(v)

def print_results():
    global y
    for v in y:
        print v 

x = get_args()
process_data(x)
print_results()
