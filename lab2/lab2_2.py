# A = 10cm, B = 10cm, C = 6cm
import numpy as np
from seaborn import heatmap

class Object:
    
    def __init__(self, resolution=30, K = 2700, cw=900, p=237, dt = 0.1, time = 120): #resolution must be multiple of 30! (when res = 30,  1 square - 1 cm)
        
        #SIMULATION PARAMETERS
        
        self.elapsed_time = 0
        self.dt = dt
        self.time = time
        self.iter_nums = int(time/dt)
        self.resolution = resolution

        #CONSTRUCTION OF SHAPE
        self.shape = np.ones((resolution, resolution)) * 20
        
        self.last_shape = self.shape.copy()

        #BOUNDARY CONDITIONS

        #0 - outside of the simulation
        self.mode = np.zeros((resolution, resolution))
        #2 - 2nd boundary condidtion
        self.mode[int(resolution/3):int(resolution*2/3), :] = 2
        self.mode[:,int(resolution/3):int(resolution*2/3)] = 2

        res = int(self.resolution/3)

        #DOTS

        self.mode[res, 0] = 4
        self.mode[0, res] = 4

        self.mode[2*res-1, 0] = 5
        self.mode[3*res-1, res] = 5

        self.mode[0, 2*res-1] = 6
        self.mode[res, 3*res-1] = 6

        self.mode[2*res-1, 3*res-1] = 7
        self.mode[3*res-1, 2*res-1] = 7

        #LINES

        self.mode[0, res+1:res*2-1] = 8
        self.mode[res, 1:res+1] = 8
        self.mode[res, 2*res-1:3*res-1] = 8

        self.mode[3*res-1, res+1:res*2-1] = 9
        self.mode[2*res-1, 1:res+1] = 9
        self.mode[2*res-1, 2*res-1:3*res-1] = 9

        self.mode[res+1:res*2-1, 0] = 10
        self.mode[1:res+1, res] = 10
        self.mode[2*res-1:3*res-1, res] = 10

        self.mode[res+1:res*2-1, 3*res-1] = 11
        self.mode[1:res+1, 2*res-1] = 11
        self.mode[2*res-1:3*res-1, 2*res-1] = 11

        #1 - normal simualtion rules
        self.mode[int(resolution/3+1):int(resolution*2/3-1), 1:resolution-1] = 1
        self.mode[1:resolution-1,int(resolution/3+1):int(resolution*2/3-1)] = 1
        #3 - heater
        self.mode[int(resolution*2/5):int(resolution*3/5), int(resolution*2/5):int(resolution*3/5)] = 3



        #Properties of an object
        self.K = K
        self.cw = cw
        self.p = p

        #print(0.25*0.01**2*self.cw*self.p/self.K/10)

    def draw(self):

        print(self.shape)

    def calc_temp(self, T_prev, T_left, T_right, T_top, T_down):

        dx = 3/self.resolution
        dy = dx


        p1 = T_prev
        p2 = (self.K*self.dt*(T_left-2*T_prev+T_right))/(self.cw*self.p*dx**2)
        p3 = (self.K*self.dt*(T_top-2*T_prev+T_down))/(self.cw*self.p*dy**2)
        
        return p1 + p2 + p3

    def update_mesh(self):
        self.last_shape = self.shape.copy()
        for iy, ix in np.ndindex(self.mode.shape):

            cell = self.mode[iy, ix]

            if cell == 1:
                self.shape[iy, ix] = self.calc_temp(self.shape[iy, ix],self.shape[iy, ix-1], self.shape[iy, ix+1], self.shape[iy+1, ix], self.shape[iy-1, ix])
            elif cell == 3:
                self.shape[iy, ix] = self.calc_temp(self.shape[iy, ix],self.shape[iy, ix-1], self.shape[iy, ix+1], self.shape[iy+1, ix], self.shape[iy-1, ix])
                if self.elapsed_time < 10:
                    self.shape[iy, ix] += self.heater_math(P = 100)
            elif cell == 4:
                self.shape[iy, ix] = self.shape[iy+1, ix+1]
            elif cell == 5:
                self.shape[iy, ix] = self.shape[iy-1, ix+1]
            elif cell == 6:
                self.shape[iy, ix] = self.shape[iy+1, ix-1]
            elif cell == 7:
                self.shape[iy, ix] = self.shape[iy-1, ix-1]
            elif cell == 8:
                self.shape[iy, ix] = self.shape[iy+1, ix]
            elif cell == 9:
                self.shape[iy, ix] = self.shape[iy-1, ix]
            elif cell == 10:
                self.shape[iy, ix] = self.shape[iy, ix+1]
            elif cell == 11:
                self.shape[iy, ix] = self.shape[iy, ix-1]
        
        self.elapsed_time += self.dt

    def heater_math(self, P, B_2 = 0.0036, h = 0.002):

        dT = P*self.dt/(self.cw*B_2*h*self.p)
        return dT
    
    def absolute_mean(self):
        """
        Helper function to calculate change in heat distribution after single iteration
        """

        arr = np.absolute(self.shape - self.last_shape)
        suma = np.sum(arr)
        return suma
    
    def stop_condition(self) -> bool:
        """
        Function depneds wheather simualtion has ended or is still running
        """
        eps = 1 * 10**(-7)    #number not significant numerically

        if self.absolute_mean() < eps:
            return True
        else:
            return False


    def heat(self) -> int:
        """
        Simulates whole heating process with stop condition

        returns: iter_num of stop simulation
        """ 
        
        for i in range(self.iter_nums):
            
            self.update_mesh()
            
            #if i%1000 == 0:
                #print(self.absolute_mean())
                #print(self.shape[15,15]-self.shape[10, 10])

            if self.stop_condition():
                return i
            
        return -1, self.absolute_mean()


