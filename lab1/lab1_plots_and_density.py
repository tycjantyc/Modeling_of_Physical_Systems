import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from lab1 import Particle

fig, (ax1, ax2) = plt.subplots(2, 2)

#fig1 = plt.figure()

part_num = 1000
list_of_particles = [Particle() for i in range(part_num)]
iter_num = 100
bin_num = 20

def now():

    ax1[0].set_xlabel("X")

def init():
    ax1[0].cla()
    ax2[0].cla()
    ax1[1].cla()
    ax2[1].cla()

    ax1[0].set_xlim(-50, 50)
    ax1[0].set_ylim(-50, 50)
    ax1[0].set_xlabel("X")

def animate(frame):

    init()
    
    distance = []
    lista_x = []
    lista_y = []
    for part in list_of_particles:
        part.make_step()
        distance.append(part.calc_square())
        lista_x.append(part.x)
        lista_y.append(part.y)
    
    ax1[0].scatter(lista_x, lista_y, marker = 'o')
    ax1[1].hist(lista_x, bin_num, range = ((-50, 50)))
    ax2[0].hist(lista_y, bin_num,range = ((-50, 50)))
    #ax2[1].hist(distance, bin_num, range = ((-50, 50)))

    #plt.cla()
    ax2[1].hist2d(lista_x, lista_y, 30, range = ((-50, 50),(-50, 50)))
    
# Create FuncAnimation object and plt.show() to show the updated animation
ani = FuncAnimation(fig, animate, frames = np.linspace(1,1000,1000), interval = 50, init_func=now)
plt.show()