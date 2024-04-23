import numpy as np
import pandas as pd
import scipy.integrate as integrate

def load_prn(file_path):
    
    df = pd.read_csv(file_path, delimiter='\t', header=None)

    x, y = [], []
    for i in df[0]:
        i = i.strip()
        a = i.split(" ")
        x.append(float(a[0]))
        y.append(float(a[-1]))

    return (x, y)

def piston_flow(x, t_t):
    
    eps = 1e-6

    if abs(x - t_t) < eps:
        return 1    #np.inf #1/(2*eps) 
    
    else:
        return 0
    
def exp_model(x, t_t):

    return (1/t_t) * np.exp((-x)/t_t)

def disp_model(x, t_t, Pe):

    p1 = (4*np.pi*Pe*x/t_t)**(-0.5)
    p2 = (1/x) * np.exp(-((1 - (x/t_t))**2)/(4*Pe*x/t_t))

    return p1*p2

def integral_func(t_, t, C_in, g, lamb):
        
        return C_in(t_)*g(t - t_)*np.exp(-lamb*(t - t_))

def integral_1(t, C_in, g, lamb):

    return integrate.quad(integral_func, -np.inf, t, args=(t, C_in, g, lamb))

def integral_2(t, C_in, g, lamb, disp = False):

    suma = 0
    if disp:

        for i in range(1, 2*t, 2):

            i = i/2
            suma += (integral_func(i, t, C_in, g, lamb) + integral_func(i+1, t, C_in, g, lamb))/2
    else:
        for i in range(t):

            suma += (integral_func(i, t, C_in, g, lamb) + integral_func(i+1, t, C_in, g, lamb))/2

    return suma


def integral_3(t, C_in, g, lamb):

    suma = 0

    for i in range(t+1):

        suma += integral_func(i, t, C_in, g, lamb)
    
    return suma

def MSE(l1, l2):
    
    if len(l1) == len(l2):
        pass
    else:
        print(f"Bad lists! {len(l1)} and {len(l2)}")

        return "Bad" 

    mse = 0

    for a, b in zip(l1, l2):

        mse += abs(a-b)**2

    return mse/len(l1)
