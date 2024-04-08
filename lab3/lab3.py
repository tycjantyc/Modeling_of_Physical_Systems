import numpy as np

S = 1366 #W/m^2 - solar constant
o = 5.67*10**-8 # W/(m^2*K^4) - stefan-boltzman constant
A = 5.1006 * 10**14 #m^2 - surface area of the Earth
c = 2.7 # W/(m^2*K)

def solar_in(albedo  = 0.3) -> float:

    return S*A/4*(1-albedo)

def solar_out(T:float, epsilon = 0.63) -> float:

    return o*T**4*A*epsilon

def solar_bal(T):
    return solar_in() - solar_out(T)

def balance_earth(T_s, T_a,S_param = 1.0, t_a = 0.53, a_s = 0.19,a_a2 = 0.31):
    
    if T_s<(273.15-10):
        pass
        #a_a2 = 0.63

    S_new = S*S_param
    return (-t_a)*(1-a_s)*S_new/4 + c*(T_s - T_a) + o*T_s**4*(1-a_a2) - o*T_a**4

def balance_atmosphere(T_s, T_a,S_param = 1.0, t_a = 0.53, a_s = 0.19,a_a = 0.30, a_a2 = 0.31, t_a2 = 0.06):
    
    if T_s<(273.15-10):
        a_a = 0.63
        #a_a2 = 0.63

    S_new = S*S_param
    return -(1 -a_a - t_a + a_s*t_a)*S_new/4 - c*(T_s - T_a) - o*T_s**4*(1-t_a2-a_a2) + 2*o*T_a**4

def balance_set(vars):

    if len(vars)==3:
        T_s, T_a, S_param = vars
        return [balance_earth(T_s, T_a, S_param), balance_atmosphere(T_s, T_a, S_param)]
    
    elif len(vars)==2:
        T_s, T_a = vars
        return [balance_earth(T_s, T_a), balance_atmosphere(T_s, T_a)]