import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from lab2 import Object
from matplotlib.ticker import LinearLocator
from matplotlib import cm

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

obj = Object(resolution=30, K = 2700, cw = 900, p = 237, dt = 0.1, time = 200)

X, Y = np.meshgrid(range(obj.resolution), range(obj.resolution))

def clear():

    ax.cla()

def animate(frame):
    
    obj.update_mesh()

    Z = obj.shape

    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                        linewidth=0, antialiased=False)
    
    ax.set_title(f"Time - {round(frame, 2)} seconds \n dt = 0.1")

    
# Create FuncAnimation object and plt.show() to show the updated animation

ax.zaxis.set_major_locator(LinearLocator(10))


ax.zaxis.set_major_formatter('{x:.02f}')

#fig.colorbar(surf, shrink=0.5, aspect=5)
print(np.linspace(0,obj.time,(obj.iter_nums+1)))
ani = FuncAnimation(fig, animate, frames = np.linspace(0,obj.time,(obj.iter_nums+1)), interval = 100)
plt.show()