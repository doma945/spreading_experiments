import numpy as np
import matplotlib.pyplot as plt

from graph import get_graph
from country import Country

args = {
    "logfile": "data/d1.csv",
    "max_iter":200,
    "beta": 0.01,
    "beta_super":0.9,
    "I_time": 5,
    "p_super": 0.35,
    "graph":"grid",
    "grid_size":50,
    "seed":1
}

np.random.seed(args["seed"])

if __name__ == "__main__":
    graph = get_graph(args={"type":args["graph"], "n": args["grid_size"]})
    
    country = Country(args, graph)
    country.run()