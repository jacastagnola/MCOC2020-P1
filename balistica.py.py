import scipy as sp
from scipy.integrate import odeint
import matplotlib.pylab as plt

#parametros y unidades
g=9.81 # m/s**2
m=15. #kg 
V=[ 0.,10.,20.] #vel viento
ro=1.225 #kg/m**3
cd=0.47
cm=0.01 #m
inch=2.54*cm
D=8.5*inch
r=D/2
A=sp.pi*r**2

CD= 0.5*ro*cd*A

# z=[x,x,vx,vy]
#dz/dt=bla(z,t)



# funcion a integrar
#vector de estado
#z=[x,y,vx,vy]
#dz/dt bala(z,t)

#                     dz1/dt=z2

#       [ z2      ]
#dz/dt= [         ]   (modelo)
#       [ FD/m-g  ]

#vector de estado
# z[0]-> x
# z[1]-> y
# z[2]-> vx
# z[3]-> vy

for i in V:
    
    def bala(z,t):
        zp=sp.zeros(4)
        zp[0]=z[2]
        zp[1]=z[3]
        v=z[2:4]    #saca las ultimas dos componentes
        v[0]=v[0]-i
        v2=sp.dot(v,v)
        vnorm=sp.sqrt(sp.dot(v,v))
        FD=-CD**v2*(v/vnorm)
        zp[2]=FD[0]/m
        zp[3]=FD[1]/m-g
        
        return zp
    
    #vector tiempo
    
    t=sp.linspace(0,6,1001)
    
    
    
    vi=100*1000./3600
    
    #parte en el origen y tiene vx=vy=10m/s
    
    z0=sp.array([0,0,vi,vi])
    
    sol= odeint(bala,z0,t)
    
   
    
    x=sol[:,0]
    y=sol[:,1]
    
    plt.plot(x,y, label=f"V={i} m/s")
    fig=plt.figure(1)


plt.xlabel('X [m]')
plt.ylabel('Y [m]')
plt.title('Trayectoria para distintos vientos')
plt.axis([0, 150, 0, 50])
plt.yticks([0, 10, 20, 30, 40, 50])
plt.legend()
plt.grid()
plt.show()
plt.tight_layout()
fig.savefig('balistica.png')