import csv
import numpy as np
import networkx as nx
from numba import jit
import matplotlib.pyplot as plt

from plot import viewer,plot_log
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

class Country:
    def __init__(self, args, graph):
        self.iter = 0
        self.images = []

        self.args = args
        self.graph = graph
        self.N = len(graph.nodes)
        self.pos = nx.get_node_attributes(self.graph, "pos")

        # === Init states ===
        self.init_states()

        # === Infect some agents ===
        n = int(np.sqrt(self.N))
        c = n//2
        inf_nodes = np.array([n*(c-1)+c-1, n*(c-1)+c, n*(c-1)+c+1, n*c+c-1, n*c+c, n*c+c+1, n*(c+1)+c-1, n*(c+1)+c, n*(c+1)+c+1])
        self.states[inf_nodes] = np.array([10,1,10,1,10,1,10,1,10])
        self.timers[inf_nodes] = args["I_time"]+1

    def run(self):
        for i in range(self.args["max_iter"]):
            self.step()
        
        print('')
        #viewer(self.images)
        plot_log(self.args["logfile"], self.pos, self.neighs, self.args)

    def step(self):
        print("\rStep {}".format(self.iter), end = '')

        p_super = self.args["p_super"]
        beta = self.args["beta"]
        beta_super = self.args["beta_super"]

        I_time = self.args["I_time"]
        # === Infections ===
        Country.update_neighs(self.states, self.indexes, self.timers,
                              self.neighs, p_super, beta, beta_super, I_time)

        #self.save_plot()
        self.log_csv()
        self.iter+=1


    @jit(nopython = True)
    def update_neighs(states, indexes, timers, neighs, p_super, beta, beta_super, I_time):
        # 0 : Suscepted
        # 1 : Infected
        # 10: Super Infected
        neigh_arr = neighs[0]
        slices = neighs[1]

        states[timers==1]=0
        timers[timers>0]-=1

        for ind in indexes:
            adj_list = neigh_arr[slices[ind][0]:slices[ind][1]]
            S_adj_list = adj_list[states[adj_list]==0]

            #if(states[ind]>0 and timers[ind]==I_time-1):
            if(states[ind]>0):
                # === Choose infected: ===
                if(states[ind]==10):
                    #infected = S_adj_list
                    new_inf_num = np.random.binomial(S_adj_list.size, beta_super)
                    infected = np.random.choice(S_adj_list, replace = False, size=new_inf_num)
                else:
                    new_inf_num = np.random.binomial(S_adj_list.size, beta)
                    infected = np.random.choice(S_adj_list, replace = False, size=new_inf_num)
                
                states[infected] = -1
                timers[infected] = I_time

                # === Choose super infected ===
                new_super_inf_num = np.random.binomial(infected.size, p_super)
                focus = np.random.choice(infected, replace = False, size=new_super_inf_num)
                states[focus] = -10

        for i,s in enumerate(states):
            if s<0:
                states[i]=abs(s)

    # === Helper Functions ===
    def get_neigh_flattened(self, neighs):
        arr = []
        slices = np.zeros(shape = (len(neighs),2))
        ind = 0
        for i,adj_list in enumerate(neighs):
            n = len(adj_list)
            slices[i] = (ind, ind+n)
            arr += adj_list

            ind += n

        return (np.array(arr, dtype = np.int32), slices)

    def init_states(self):
        #self.states = np.array(["S"]*self.N)
        self.states = np.zeros(self.N, dtype = np.int8)
        self.indexes = np.array(np.arange(self.N, dtype= np.int32))
        self.timers = np.zeros(self.N, dtype = np.int8)
        
        all_neighs = []
        indexes = nx.get_node_attributes(self.graph, "index")
        for name in self.graph.nodes():
            neighs = [indexes[neigh] for neigh in self.graph[name].keys()]
            all_neighs.append(neighs)

        self.neighs = self.get_neigh_flattened(all_neighs)

    def save_plot(self):
        #pos = nx.get_node_attributes(self.graph, "pos")
        b = (0,0,1)
        r = (1,0,0)
        o = (1,0.5,0)
        g = (0,1,0)

        dict = {0:g, 1:(1,1,0), 10:r}

        nx.draw(self.graph, self.pos, node_size =100, node_color = [dict[state] for state in self.states],
            title = "www")
        canvas = FigureCanvas(plt.gcf())
        s, (width, height) = canvas.print_to_buffer()
        img = np.fromstring(s, np.uint8).reshape((height, width, 4))

        plt.close(plt.gcf())

        self.images.append(img)

    def log_csv(self):
        # === Delete previous logs ===
        if self.iter == 0:
            with open(self.args["logfile"], 'w') as f:
                pass
        
        with open(self.args["logfile"], 'a') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            act_iter_info = [self.iter]
            act_iter_info += list(self.states)
            csv_writer.writerow(act_iter_info)

        
