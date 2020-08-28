

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint
import scipy as sp

km = 1000 
pi = np.pi
mt = 5.972*10**24   # Masa tierra [kg]
Rdt = 6371.*km      # Radio tierra [m]
omeg_t=2*pi/86400.  # Rapidez angular tierra [rad/s]
G = 6.673*10**(-11) # Const. Gravitacional [N*m2/kg*2]
ms = 2300.          # Masa satelite [kg]


def Sentinel(z,t):
    zp=sp.zeros(4)
    zp[0] = z[2]
    zp[1] = z[3]
    zp[2] = (z[0])*z[3]*z[3]-G*mt/((z[0])*(z[0]))
    zp[3] = -2*z[2]*z[3]/(z[0])
    
    return zp


t = np.linspace(0,100000,1001)

z = np.array([Rdt+80*km,0,0,1.241*10**(-3)])
solve = odeint(Sentinel, z, t)
x1= solve[:,0]
y1 = solve[:,1]+omeg_t*t
y2 = solve[:,1]


z1 = np.array([Rdt+80*km,0,0,1.24611*10**(-3)])
solve_1 = odeint(Sentinel, z1, t)
x3 = solve_1[:,0]
y3 = solve_1[:,1]+omeg_t*t


theta = np.linspace(0,2*pi,1001)
theta2 = np.linspace(0,60*pi,1001)

rad_tierra = np.linspace(Rdt,Rdt,1001)
atm = np.linspace(Rdt+1000*km, Rdt+1000*km, 1001)
lim_inf_sat = np.linspace(Rdt+80*km, Rdt+80*km, 1001)
lim_sup_sat = np.linspace(Rdt+700*km, Rdt+700*km, 1001)


fig = plt.figure(figsize=(20,20))  
plt.subplot
ax = fig.add_subplot(2,3,5, projection="polar")
ax.plot(y1,x1,color="cyan",linewidth=0.5, label='Satelite')
ax.plot(theta,rad_tierra,color="brown",linewidth=2, label='Superficie de la Tierra')
ax.plot(theta,atm,color="blue",linewidth=2, label='Límite de la atmosfera')
ax.plot(theta,lim_inf_sat,color="black",linewidth=2, label='Limite inferior satelite')
ax.plot(theta,lim_sup_sat,color="black",linewidth=2, label='Limite superior satelite')

ylabels = ['$%d \\cdot 10^6$' % (ytick / 1e6) for ytick in ax.get_yticks()]
ax.set_yticklabels(ylabels, fontsize=12)

fig.legend(loc="lower center", fontsize=16)

ax.set_title('movimiento respecto eje de la tierra', fontsize=20)
graf = fig.add_subplot(2,3,2)
graf.plot(y1,x1,color="red",linewidth=1, label='Satelite')
graf.plot(theta2,rad_tierra,color="brown",linewidth=2, label='Superficie de la Tierra')
graf.plot(theta2,atm,color="blue",linewidth=2, label='Límite de la atmosfera')
graf.plot(theta2,lim_inf_sat,color="black",linewidth=2, label='Limite inferior satelite')
graf.plot(theta2,lim_sup_sat,color="black",linewidth=2, label='Limite superior satelite')
graf.set_xlim([0, 100])
graf.set_xlabel("Theta [rad]")
graf.set_ylabel("Elevacion [m]")

graf2 = fig.add_subplot(2,3,1)

graf2.plot(y3,x1,color="red",linewidth=1, label='Satelite')
graf2.plot(theta2,rad_tierra,color="brown",linewidth=2, label='Superficie de la Tierra')
graf2.plot(theta2,atm,color="blue",linewidth=2, label='Límite de la atmosfera')
graf2.plot(theta2,lim_inf_sat,color="black",linewidth=2, label='Limite inferior satelite')
graf2.plot(theta2,lim_sup_sat,color="black",linewidth=2, label='Limite superior satelite')
graf2.set_xlim([0, 100])
graf2.set_xlabel("Theta [rad]")
graf2.set_ylabel("Elevacion [m]")

ax2 = fig.add_subplot(2,3,4, projection="polar")
ax2.plot(y2,x1,color="cyan",linewidth=0.5, label='Satelite')
ax2.plot(theta,rad_tierra,color="brown",linewidth=2, label='Superficie de la Tierra')
ax2.plot(theta,atm,color="blue",linewidth=2, label='Límite de la atmosfera')
ax2.plot(theta,lim_inf_sat,color="black",linewidth=2, label='Limite inferior satelite')
ax2.plot(theta,lim_sup_sat,color="black",linewidth=2, label='Limite superior satelite')

ax2.set_title('Movimiento respecto eje satelite', fontsize=20)
ylabels = ['$%d \\cdot 10^6$' % (ytick / 1e6) for ytick in ax.get_yticks()]
ax2.set_yticklabels(ylabels, fontsize=12)



graf3 = fig.add_subplot(2,3,3)
graf3.plot(y3,x3,color="red",linewidth=1, label='SATELITE')
graf3.plot(theta2,rad_tierra,color="brown",linewidth=2, label='Superficie de la Tierra')
graf3.plot(theta2,atm,color="blue",linewidth=2, label='Límite de la atmosfera')
graf3.plot(theta2,lim_inf_sat,color="black",linewidth=2, label='Limite inferior satelite')
graf3.plot(theta2,lim_sup_sat,color="black",linewidth=2, label='Limite superior satelite')
graf3.set_xlim([0, 100])
graf3.set_xlabel("Theta [rad]")
graf3.set_ylabel("Elevacion [m]")

ax3 = fig.add_subplot(2,3,6, projection="polar")
ax3.plot(y3,x3,color="cyan",linewidth=0.5, label='Satelite')
ax3.plot(theta,rad_tierra,color="brown",linewidth=2, label='Superficie de la Tierra')
ax3.plot(theta,atm,color="blue",linewidth=2, label='Límite de la atmosfera')
ax3.plot(theta,lim_inf_sat,color="black",linewidth=2, label='Limite inferior satelite')
ax3.plot(theta,lim_sup_sat,color="black",linewidth=2, label='Limite superior satelite')
ylabels = ['$%d \\cdot 10^6$' % (ytick / 1e6) for ytick in ax.get_yticks()]
ax3.set_yticklabels(ylabels, fontsize=12)
ax3.set_title('movimiento hasta 700 km', fontsize=20)




plt.tight_layout()
fig.savefig('Sentinel.png')