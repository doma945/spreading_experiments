import numpy as np
import networkx as nx
#from numba import jit

class Country:
    def __init__(self, args, graph):
        self.args = args
        self.graph = graph
        self.N = len(graph.nodes)
        self.iter = 0

        # === Init states ===
        self.states = np.array(["S"]*self.N)
        self.indexes = np.ndarray(self.N)
        self.neighs = []

        indexes = nx.get_node_attributes(graph, "index")
        for name in graph.nodes():
            neighs = [indexes[neigh] for neigh in graph[name].keys()]
            self.neighs.append(neighs)

        self.neighs = np.array(self.neighs)

    def run(self):
        for i in range(self.args["max_iter"]):
            self.step()

    def step(self):
        print("Step {}".format(self.iter))
        self.iter+=1