import numpy as np
import matplotlib.pyplot as plt

from graph import get_graph
from country import Country

#args = {
#    "logfile": "data/d1.csv",
#    "max_iter":200,
#    "beta": 0.0,
#    "beta_super":0.6,
#    "I_time": 5,
#    "p_super": 0.2,
#    "graph":"barabasi",
#    "grid_size":500,
#    "seed":1,
#}
args = {
    "logfile": "data/d1.csv",
    "max_iter":200,
    "beta": 0.0,
    "beta_super":1.0,
    "I_time": 5,
    "p_super": 0.37,
    "graph":"grid",
    "grid_size":30,
    "seed":3,
}

np.random.seed(args["seed"])

if __name__ == "__main__":
    graph = get_graph(args={"type":args["graph"], "n": args["grid_size"]})
    #graph = get_graph(args={"type":args["graph"], "n": args["grid_size"], "m":2})
    
    country = Country(args, graph)
    country.run()