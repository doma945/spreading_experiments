import networkx as nx
import matplotlib.pyplot as plt

def get_graph(args):
    if args["type"] == "grid":
        return grid(args)
    else:
        print("Type not understood")

def grid(args):
    n = args["n"]
    graph = nx.Graph()

    # === Init nodes ===
    ind = 0
    for i in range(n):
        for j in range(n):
            graph.add_node("{},{}".format(i,j),pos = (i,j),
                           name = "{},{}".format(i,j), index=ind)
            ind+1
    # === Init edges ===
    for i in range(n-1):
        for j in range(n-1):
            graph.add_edge("{},{}".format(i,j),"{},{}".format(i,j+1))
            graph.add_edge("{},{}".format(i,j),"{},{}".format(i+1,j))
            
        graph.add_edge("{},{}".format(i,n-1),"{},{}".format(i+1,n-1))
        graph.add_edge("{},{}".format(n-1,i),"{},{}".format(n-1,i+1))

    pos = nx.get_node_attributes(graph, "pos")
    #names = nx.get_node_attributes(graph, "name")
    b = (0,0,1)
    nx.draw(graph, pos, node_size =1, node_color = [b for i in range(len(pos))])
    plt.show()
    return graph