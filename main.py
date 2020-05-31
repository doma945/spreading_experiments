import numpy as np
import matplotlib.pyplot as plt

from graph import get_graph
from country import Country

args = {
    "max_iter":10,
    "beta": 0.37,
    "I_time": (lambda n: 5*np.ones(n, dtype=np.int32)),
    "super_I": 0.3,
}

if __name__ == "__main__":
    graph = get_graph(args={"type":"grid","n":50})
    
    country = Country(args, graph)
    country.run()