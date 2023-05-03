import sys
import json
import argparse
from time import perf_counter
sys.path.append('../Algorithms')
from basic_algos import *
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--curve",
                        default="Basic", choices=["P-192", "P-224", "P-256", "P-384", "Basic"])
    parser.add_argument("-a", "--algo",
                        default="rDnA", 
                        choices= ["DnA", "rDnA", "ML", "JDnA"])
    parser.add_argument("-k", "--scalar", type=int, default=10)
    args = parser.parse_args()
    curve = args.curve
    algo = args.algo
    k = args.scalar
    fname = f'../curves/{args.curve}.json'
    with open(f'../curves/{args.curve}.json') as file:
        data = json.load(file)
        p = int(data['field']['p'],0)
        a = int(data['params']['a']['raw'],0)
        b = int(data['params']['b']['raw'],0)
        P = (int(data['generator']['x']['raw'],0),
             int(data['generator']['y']['raw'],0))
    if(algo == "DnA"):
        st = perf_counter()
        for i in range(1,k):
            DoubleAndAdd(i, P, a, p)
        print(perf_counter() - st)
    elif(algo == "rDnA"):
        st = perf_counter()
        for i in range(1,k):
            recursive_DnA(P, i, a, p)
        print(perf_counter() - st)
    elif(algo == "ML"):
        st = perf_counter()
        for i in range(1,k):
            MontgomeryLadder(i, P, a, p)
        print(perf_counter() - st)
    elif(algo == "JDnA"):
        st = perf_counter()
        for i in range(1,k):
            JoyesDoubleandAdd(i, P, a, p)
        print(perf_counter() - st)
    
