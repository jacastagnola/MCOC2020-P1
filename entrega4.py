from scipy.integrate import odeint
import scipy as sc
import numpy as np
import matplotlib.pyplot as plt


pi = np.pi
m = 1       #kg
f = 1       #Hz
chi = 0.2
omega = 2*pi*f
k = m*omega**2 
c = 2*chi*omega*m
#condiciones iniciales
#posicion=0
#velocidad=1


def zpunto(z,t):
    zp = np.zeros(2)
    zp[0] = z[1]
    zp[1] = -(c*z[1]+k*z[0])/m
    return zp

def eulerint(zp,z0,t,Nsub=1):
    Nt=len(t)
    Ndim=len(z0)
    z = np.zeros((Nt, Ndim))
    z[0,:] = z0
    
    for i in range(1,Nt):
        t_ant = t[i-1]
        dt=(t[i]-t[i-1])/Nsub
        z_temp = z[i-1,:]*1.0
        for k in range(Nsub):
            z_temp+=dt*zp(z_temp,t_ant+k*dt)
        z[i,:]=z_temp
    return z

z0=np.array([0,1]) #vector condiciones iniciales

t=np.linspace(0,4,100) #vector de tiempo

armonico_real=1/omega*np.exp(-c/(2*m)*t)*np.sin(omega*t) #respuesta analitica

solve=odeint(zpunto,z0,t) #solucion con odeint

solve_eu1=eulerint(zpunto,z0,t,1) #solucion con metodo de integracion euler implementado mas arriba para distintas divisiones
solve_eu10=eulerint(zpunto,z0,t,10)
solve_eu100=eulerint(zpunto,z0,t,100)

x_odeint= solve[:,0]    
x_eu1= solve_eu1[:,0]
x_eu10=solve_eu10[:,0]
x_eu100=solve_eu100[:,0]

fig = plt.figure(figsize=(10,10)) 
ax = fig.add_subplot(1,1,1)
ax.plot(t,armonico_real, color="black", linewidth=2, label="Analitica")
ax.plot(t,x_odeint, color="blue", linewidth=2, label="Odeint")
ax.plot(t,x_eu1, color="green", linestyle="--", linewidth=2, label="euler Ndiv=1")
ax.plot(t,x_eu10, color="red", linestyle="--", linewidth=2, label="euler Ndiv=10")
ax.plot(t,x_eu100, color="orange", linestyle="--", linewidth=2, label="euler Ndiv=100")
ax.set_xlabel("TIEMPO [seg]")
ax.set_ylabel("X [m]")
plt.tight_layout()
plt.grid()
plt.legend(title="Tipos de respuesta")
plt.show()

fig.savefig('Grafico entrega 4.png')









