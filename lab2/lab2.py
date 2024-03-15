# A = 10cm, B = 10cm, C = 6cm
import numpy as np


class Object:
    
    def __init__(self, resolution=30, K = 2700, cw=900, p=237): #resolution must be multiple of 30! (when res = 30,  1 square - 1 cm)
        
        self.resolution = resolution
        self.shape = np.zeros((resolution, resolution))
        #cold rim
        self.shape[int(resolution/3):int(resolution*2/3), :] = 10
        self.shape[:,int(resolution/3):int(resolution*2/3)] = 10
        #normal temp center
        self.shape[int(resolution/3+1):int(resolution*2/3-1), 1:resolution-1] = 20
        self.shape[1:resolution-1,int(resolution/3+1):int(resolution*2/3-1)] = 20
        #hot heater
        self.shape[int(resolution*2/5):int(resolution*3/5), int(resolution*2/5):int(resolution*3/5)] = 80

        self.last_shape = self.shape.copy()

        #BOUNDARY CONDITIONS
        #0 - outside of the simulation
        self.mode = np.zeros((resolution, resolution))
        #2 - 2nd boundary condidtion
        self.mode[int(resolution/3):int(resolution*2/3), :] = 2
        self.mode[:,int(resolution/3):int(resolution*2/3)] = 2
        #1 - normal simualtion rules
        self.mode[int(resolution/3+1):int(resolution*2/3-1), 1:resolution-1] = 1
        self.mode[1:resolution-1,int(resolution/3+1):int(resolution*2/3-1)] = 1
        #3 - 1st boundary condition
        self.mode[int(resolution*2/5):int(resolution*3/5), int(resolution*2/5):int(resolution*3/5)] = 3

        self.K = K
        self.cw = cw
        self.p = p

    def draw(self):

        print(self.shape)

    def calc_temp(self, T_prev, T_left, T_right, T_top, T_down, dt):
        dx = self.resolution/300
        dy = dx

        p1 = T_prev
        p2 = (self.K*dt*(T_left-2*T_prev+T_right))/(self.cw*self.p*dx**2)
        p3 = (self.K*dt*(T_top-2*T_prev+T_down))/(self.cw*self.p*dy**2)
        
        return p1 + p2 + p3

    def update_mesh(self, dt):
        self.last_shape = self.shape.copy()
        for iy, ix in np.ndindex(self.mode.shape):
            if self.mode[iy, ix] == 1:
                self.shape[iy, ix] = self.calc_temp(self.shape[iy, ix],self.shape[iy, ix-1], self.shape[iy, ix+1], self.shape[iy+1, ix], self.shape[iy-1, ix], dt)

        

    def stop_condition(self):

        arr = np.absolute(self.shape - self.last_shape)
        print(arr)
        suma = np.sum(arr)

        return suma

    def heat(self):
        pass
        #simulates whole heating process with stop condition
            


