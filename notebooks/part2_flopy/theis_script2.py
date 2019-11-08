import numpy as np
import matplotlib.pyplot as plt
import scipy.special as sps

def drawdown(Q=1.16, T=0.30, S=0.0008, r=1000, t=1.):
    u = r**2. * S / (4. * T * t)
    return (Q / (4. * np.pi * T)) * sps.exp1(u)

def distance(xw, yw, x, y):
    return np.sqrt((y-yw)**2 + (x-xw)**2)

def time_setup(perlen=86400, tsmult=1.2,nstp=50):
    t = []
    perlen = 86400.
    tsmult = 1.2
    nstp = 50
    dt = perlen*((tsmult-1.)/(tsmult**nstp - 1.))
    t.append(dt)  
    for i in range(1, nstp):
        dt *= tsmult
        t.append(t[i-1] + dt)
    t = np.array(t)
    print(t.shape, t[-1])  
    return t
    
def theis_analytical(t, printout=False):

    x = np.linspace(-1050., 1050, 21)
    X, Y = np.meshgrid(x, x)
    r = distance(0., 0., X, Y)

    all_s = []

    for idx, tt in enumerate(t):
        print('{}'.format(idx))
        s = drawdown(t=tt, r=r)
        if printout == True:
            plt.savefig('{:04d}.png'.format(idx))
            plt.imshow(s, vmin=0, vmax=1.5, interpolation='nearest')
            plt.title('{:6.4f} hours'.format(tt/3600.))
            plt.colorbar()
            plt.close()
        all_s.append(s)
        


    print(drawdown(t=86400))

    print('the end')

    return all_s
