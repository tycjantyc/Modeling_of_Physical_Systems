import numpy as np

def script(my_nx = 100, C = 0.5):

    def psi_0(x):
    
        a = 5
        return 8*a**3 / (x**2 + 4*a**2)

    nx = my_nx
    x, dx = np.linspace(-100, 300, nx, endpoint=False, retstep=True)

    u = 2
    t_max = 50

    # algorithm coded in Python/NumPy:

    def flux(psi_l, psi_r, C):
        return .5 * (C + abs(C)) * psi_l + \
            .5 * (C - abs(C)) * psi_r

    class shift:
        def __radd__(self, i): 
            return slice(i.start+1, i.stop+1)
        def __rsub__(self, i): 
            return slice(i.start-1, i.stop-1)

    def upwind(psi, i, C):
        return psi[i] - flux(psi[i    ], psi[i+one], C[i]) + \
                        flux(psi[i-one], psi[i    ], C[i-one]) 
    
    i = slice(1,nx-2)
    one = shift()

    nt = int(nx/(4*C))
    dt = t_max / nt

    C = u * dt / dx
    C_phys = np.full(nx-1, C)

    psi_upwind = psi_0(x)
    for _ in range(nt):
        psi_upwind[i] = upwind(psi_upwind, i, C_phys)


    def C_corr(C, nx, psi):
        j = slice(0, nx-1)
        return (abs(C[j]) - C[j]**2) * (psi[j+one] - psi[j]) / (psi[j+one] + psi[j])

    psi_mpdata = psi_0(x)
    for _ in range(nt):
        psi_mpdata[i] = upwind(psi_mpdata, i, C_phys)
        psi_mpdata[i] = upwind(psi_mpdata, i, C_corr(C_phys, nx, psi_mpdata))

    psi_analytic = psi_0(x - u * t_max)

    return dx, psi_upwind, psi_mpdata, psi_analytic
