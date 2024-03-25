import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
from lab2_2 import Object
from matplotlib.ticker import LinearLocator
from matplotlib import cm
import os

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

obj = Object(resolution=30, K = 237*1000, cw = 900, p = 2700, dt = 0.01, time = 30)

X, Y = np.meshgrid(range(obj.resolution), range(obj.resolution))

def clear():

    ax.clear()

def animate(frame):
    
    obj.update_mesh()
    clear()
    Z = obj.shape

    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                        linewidth=0, antialiased=False)
    
    ax.set_title(f"Alumina heat - Time - {round(frame, 2)} seconds \n dt = {0.01}")
    return ax

    
# Create FuncAnimation object and plt.show() to show the updated animation

ax.zaxis.set_major_locator(LinearLocator(10))


ax.zaxis.set_major_formatter('{x:.02f}')

#fig.colorbar(surf, shrink=0.5, aspect=5)
print(np.linspace(0,obj.time,(obj.iter_nums+1)))
ani = FuncAnimation(fig, animate, frames = np.linspace(0,obj.time,(obj.iter_nums+1)), interval = 10)
#FFwriter = animation.FFMpegWriter(fps=10)
#path = os.getcwd()
#fin_path = os.path.join(path, r'animation.mp4')
#ani.save(fin_path, writer = FFwriter)
plt.show()