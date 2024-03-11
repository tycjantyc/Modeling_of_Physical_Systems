import numpy as np

class Particle:
    def __init__(self, x=0, y=0):

        self.x = x
        self.y = y
        self.lista_x = [x]
        self.lista_y = [y]

    def make_step(self):

        self.x += np.random.normal(0, 1, 1)[0]
        self.y += np.random.normal(0, 1, 1)[0]

        self.lista_x.append(self.x)
        self.lista_y.append(self.y)

    def get_x(self):
        return self.lista_x
    
    def get_y(self):
        return self.lista_y
    
    def calc_square(self):
        return self.x**2 + self.y**2






