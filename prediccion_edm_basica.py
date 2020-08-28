from matplotlib.pylab import *
from scipy.integrate import odeint
import scipy as sc
import numpy as np
hr=3600 #seg
km=1000 #mts
Radio=6371*km #km
Mt=5.972e24 #kg
G=6.67408e-11 # mts^3*kg^-1*seg^-2
omega=-7.2921150e-5 #rad/seg
HO= 700*km

FgMax=G*Mt/Radio**2

zp=np.zeros(6)
def zpunto(z,t):
    c=np.cos(omega*t)
    s=np.sin(omega*t)
    R=np.array([
        [c,s,0],
        [-s,c,0],
        [0,0,1]])
    Rp= omega*np.array([
        [-s,c,0],
        [-c,-s,0],
        [0,0,0]])
    Rpp=(omega**2)*np.array([
        [-c,-s,0],
        [s,-c,0],
        [0,0,0]])
    z1=z[0:3] #x,y,z
    z2=z[3:6] #vx,vy,vz
    r2=np.dot(z1,z1)
    r=np.sqrt(r2)
    
    Fg=(-G*Mt/r**2)*(R@(z1/r))
    
    zp[0:3]=z2
    zp[3:6]=R.T@(Fg-(2*(Rp@z2)+(Rpp@z1) ))
    
    return zp

t=np.linspace(0, 5.*hr, 1001) #vector de tiempo 

x0=Radio + HO

vt=1000.

z0=np.array([x0,0,0,0,vt,0])

sol=odeint(zpunto,z0,t)

x=sol[:, 0:3]

H=np.sqrt((x[:,0]**2+x[:,1]**2+x[:,2]**2))-Radio

from datetime import datetime

ti="2020-08-04T22:59:42.000000"
ti=ti.split("T")
ti="{} {}".format(ti[0],ti[1])
ti=datetime.strptime(ti,"%Y-%m-%d %H:%M:%S.%f")

tf="2020-08-06T00:59:42.000000"
tf=tf.split("T")
tf="{} {}".format(tf[0],tf[1])
tf=datetime.strptime(tf,"%Y-%m-%d %H:%M:%S.%f")

deltaT=(tf-ti).seconds





x_i=-1660427.548743 #metros
y_i=6754351.559859
z_i=-1312889.129784

vx_i=1874.245099  #metros/segundos
vy_i=-949.955181
vz_i=-7298.390726

x_f=-13726.265982   #metros
y_f=3457293.584017
z_f=6163714.542936

vx_f=2411.996729    #metros/segundos
vy_f=6279.207369
vz_f=-3508.712958


t1=np.linspace(0,deltaT,9361)


z01=np.array([x_i,y_i,z_i,vx_i,vy_i,vz_i])

sol1=odeint(zpunto,z0,t)

x=sol1[:,:]

pos_final=np.array([x_f,y_f,z_f,vx_f,vy_f,vz_f])-sol1[-1]

distancia=np.array([pos_final[0],pos_final[1],pos_final[2]])

a=np.linalg.norm(distancia)
print(f"{a} [m]")






    

