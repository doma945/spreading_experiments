import numpy as np
#from numba import jit

class Country:
    def __init__(self, args, graph):
        self.args = args
        self.graph = graph
        self.N = len(graph.nodes)

        self.states = np.array(["S" for g in graph.nodes])
        self.indexes = np.ndarray(self.N)

        self.iter = 0

    def run(self):
        for i in range(self.args["max_iter"]):
            self.step()

    def step(self):
        print("Step {}".format(self.iter))
        self.iter+=1