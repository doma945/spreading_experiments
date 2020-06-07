import numpy as np
import copy
import matplotlib.pyplot as plt

from graph import get_graph
from country import Country

args_0 = {
    "logfile": "data/d1.csv",
    "max_iter":200,
    "beta": 0.0,
    "beta_super":1.0,
    "I_time": 5,
    "p_super": 0.37,
    "graph":"grid",
    "grid_size":30,
    "seed":1
}


def run_with_args(args):
    np.random.seed(args["seed"])
    graph = get_graph(args={"type":args["graph"], "n": args["grid_size"]})
    
    country = Country(args, graph)
    country.run()

def m1():
    # === Measurement 1 ===
    args = copy.copy(args_0)
    for n in [30, 50]:
        args["grid_size"]=n
        for beta_super in [1.0, 0.96]:
            args["beta_super"]=beta_super
            for seed in [1,2,3]:
                args["seed"]=seed
                print(args)
                run_with_args(args)

def m2():
    # === Measurement 2 ===
    args = copy.copy(args_0)
    args["beta_super"]=0.96
    for n in [30,50]:
        args["grid_size"]=n
        for beta in [0.01, 0.05]:
            args["beta"]=beta
            for seed in [1,2]:
                args["seed"]=seed
                run_with_args(args)

def m3():
    # === Measurement 2 ===
    args = copy.copy(args_0)
    args["beta_super"]=0.9
    for n in [30,50]:
    #for n in [50]:
        args["grid_size"]=n
        for beta in [0.0, 0.01, 0.05]:
        #for beta in [0.01]:
            args["beta"]=beta
            print(args)
            run_with_args(args)

if __name__ == "__main__":
    m1()
    m2()
    m3()


                

