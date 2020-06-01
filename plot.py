import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import matplotlib.animation as animation

class Index(object):
    def __init__(self, images, img, ax):
        self.ind = 0
        self.images = images
        self.size = len(images)
        self.img = img
        self.ax = ax

    def next(self, event):
        self.ind = min(self.ind+1,self.size-1)
        self.img.set_data( self.images[self.ind])
        self.ax.set_title( "{}".format(self.ind))
        plt.draw()

    def prev(self, event):
        self.ind = max(self.ind-1,0)
        self.img.set_data( self.images[self.ind])
        self.ax.set_title( "{}".format(self.ind))
        plt.draw()

def viewer(images):
    fig, ax = plt.subplots()
    ax.set_title("0")
    img = plt.imshow(images[0])
    plt.draw()
    plt.subplots_adjust(bottom=0.2)
    callback = Index(images, img, ax)
    axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
    axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
    bnext = Button(axnext, 'Next')
    bnext.on_clicked(callback.next)
    bprev = Button(axprev, 'Previous')
    bprev.on_clicked(callback.prev)

    plt.show()

def plot_log(logfile, pos, neighs):
    # === Read data ===
    with open(logfile) as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        data = []
        for row in csv_reader:
            data.append(row)

    data = np.array(data).astype(int)
    iters = data[:,0]
    coords = np.array([v for v in pos.values()])
    N = len(iters)
    print("Iters {}".format(N))

    row = data[0,1:]
    fig, ax = plt.subplots()
    color = np.array(['b']*len(coords))
    ln = ax.scatter(coords[:,0], coords[:,1], c = color)

    def init():
        return ln,

    def update(frame):
        #print(frame[1:])
        row = data[frame,1:]
        color[row==0] = 'b'
        color[row==1] = 'y'
        color[row==10] = 'r'
        ln = ax.scatter(coords[:,0], coords[:,1], c = color)
        ax.set_title(frame)
        return ln,

    ani = animation.FuncAnimation(fig, update, frames=range(N),
                        init_func=init, blit=False, interval=100)
    plt.show()