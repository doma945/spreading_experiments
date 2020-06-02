import numpy as np
import matplotlib.pyplot as plt

from graph import get_graph
from country import Country

args = {
    "logfile": "data/d1.csv",
    "max_iter":200,
    "beta": 0.0,
    "I_time": 5,
    "p_focus": 0.37,
}

if __name__ == "__main__":
    graph = get_graph(args={"type":"grid","n":25})
    
    country = Country(args, graph)
    country.run()