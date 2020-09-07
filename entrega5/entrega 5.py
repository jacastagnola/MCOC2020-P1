import xml
import xml.etree.ElementTree as ET
from numpy import linalg as LA
from numpy import zeros
import datetime as dt
from scipy.integrate import odeint
import scipy as sc
import numpy as np
import matplotlib.pyplot as plt
from orbita_predicha import satelite
from time import perf_counter
from implementacion_J2_J3 import satelite_Js


#https://docs.python.org/3/library/xml.etree.elementtree.html

def utc2time(utc, ut1, EOF_datetime_format = "%Y-%m-%dT%H:%M:%S.%f"):
	t1 = dt.datetime.strptime(ut1,EOF_datetime_format)
	t2 = dt.datetime.strptime(utc,EOF_datetime_format)
	return (t2 - t1).total_seconds()


def leer_eof(fname):
	tree = ET.parse(fname)
	root = tree.getroot()

	Data_Block = root.find("Data_Block")		
	List_of_OSVs = Data_Block.find("List_of_OSVs")

	count = int(List_of_OSVs.attrib["count"])

	t = zeros(count)
	x = zeros(count)
	y = zeros(count)
	z = zeros(count)
	vx = zeros(count)
	vy = zeros(count)
	vz = zeros(count)

	set_ut1 = False
	for i, osv in enumerate(List_of_OSVs):
		UTC = osv.find("UTC").text[4:]
		
		x[i] = osv.find("X").text   #conversion de string a double es implicita
		y[i] = osv.find("Y").text
		z[i] = osv.find("Z").text
		vx[i] = osv.find("VX").text
		vy[i] = osv.find("VY").text
		vz[i] = osv.find("VZ").text

		if not set_ut1:
			ut1 = UTC
			set_ut1 = True

		t[i] = utc2time(UTC, ut1)

	return t, x, y, z, vx, vy, vz
from sys import argv

eofname=argv[1]


t,x,y,z,vx,vy,vz=leer_eof(eofname)

z_i= np.array([x[0], y[0], z[0], vx[0], vy[0], vz[0]]) #vector de condicion inicial

z_f=np.array([x[-1], y[-1], z[-1],vx[-1], vy[-1], vz[-1] ]) #vectori final

t1=perf_counter()
sol= odeint(satelite, z_i, t)
t2=perf_counter()
dt_odeint= t2-t1



# print(f"condicion inicial: {z_i}")
# print(f"condicion final: {z_f}")



plt.figure()
plt.subplot(3,1,1)
plt.title(f"Posicion")
plt.plot(t/3600,x/1000)
plt.plot(t/3600,sol[:,0]/1000)
plt.ylabel("X [km]")
plt.subplot(3,1,2)
plt.plot(t/3600,y/1000)
plt.plot(t/3600,sol[:,1]/1000)
plt.ylabel("Y [km]")
plt.subplot(3,1,3)
plt.plot(t/3600,z/1000)
plt.plot(t/3600,sol[:,2]/1000)
plt.xlabel("TIEMPO [horas]")
plt.ylabel("Z [km]")
plt.tight_layout()
plt.show()

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
            z_temp += dt*zp(z_temp,t_ant+k*dt)
        z[i,:]=z_temp
    return z

t3=perf_counter()
sol_eulerint=eulerint(satelite,z_i,t,1)
t4=perf_counter()
dt_eulerint= t4 - t3

diferencias = sol_eulerint-sol

diferencias=np.array(diferencias)

norma=np.sqrt(np.sum(diferencias[:,:3]**2,axis=1))

sigmamax=round(norma[-1]/1000)

print(f"SIGMA MAX {sigmamax}")
print(f"odeint se demoro {dt_odeint}")
print(f"eulerint se demoro {dt_eulerint}")

plt.figure()
plt.plot(t/3600,norma/1000)
plt.xlabel("TIEMPO [horas]")
plt.ylabel("Deriva [km]")
plt.tight_layout()
plt.grid()
plt.title(f"Distancia entre predicciones euler y odeint sigmamax={sigmamax} km")
plt.show()

# #con este codigo se va probando con diferentes N hasta que el error fuera lo mas bajo

# # N = 600
# # val_real = odeint(satelite, z_i, t)
    
# # val_calc = eulerint(satelite,z_i,t,N)

# # err = np.sqrt(np.sum(((val_calc - val_real) / val_real)**2)) * 100
# # err = np.abs((val_calc - val_real) / val_real)
# # print(N, err[-1,:]) # calculo el error para cada componente del vector
    
   
    

# t5=perf_counter()
# sol_eulerint1200=eulerint(satelite,z_i,t,1200)
# t6=perf_counter()
# dt_eulerint1200= t6-t5
# diferencias1200 = sol_eulerint1200-sol

# diferencias1200=np.array(diferencias1200)

# norma1200=np.sqrt(np.sum(diferencias1200[:,:3]**2,axis=1))

# sigmamax600=round(norma1200[-1]/1000)

# print(f"SIGMA MAX {sigmamax600}")
# print(f"eulerint con 1200 divivsiones se demora{dt_eulerint1200}")


# plt.figure()
# plt.plot(t/3600,norma1200/1000)
# plt.xlabel("TIEMPO [horas]")
# plt.ylabel("Deriva [km]")
# plt.tight_layout()
# plt.grid()
# plt.title(f"Distancia entre predicciones euler y odeint con un 5% de error sigmamax={sigmamax600} km")
# plt.show()

    
t7=perf_counter()
solJ= odeint(satelite_Js, z_i, t)
t8=perf_counter()

print(f"con la implementacion de J2 y J3 se demoro {t8-t7}"  )

plt.figure()
plt.subplot(3,1,1)
plt.title(f"Posicion implementando J2 y J3")
plt.plot(t/3600,x/1000)
plt.plot(t/3600,solJ[:,0]/1000)
plt.ylabel("X [km]")
plt.subplot(3,1,2)
plt.plot(t/3600,y/1000)
plt.plot(t/3600,solJ[:,1]/1000)
plt.ylabel("Y [km]")
plt.subplot(3,1,3)
plt.plot(t/3600,z/1000)
plt.plot(t/3600,solJ[:,2]/1000)
plt.xlabel("TIEMPO [horas]")
plt.ylabel("Z [km]")
plt.tight_layout()
plt.show()


sol = odeint(satelite, z_i, t)

pos_final=np.array([x[-1], y[-1], z[-1],vx[-1], vy[-1], vz[-1] ])-sol[-1]


dif_dist = np.array([pos_final[0],pos_final[1],pos_final[2]])
dist = LA.norm(dif_dist)
print(f"Diferencia con Modelo sin implementar mejoras {round(dist/1000)} [m]")

solJ = odeint(satelite_Js, z_i, t)

pos_finalJ=np.array([x[-1], y[-1], z[-1],vx[-1], vy[-1], vz[-1] ])-solJ[-1]


dif_dist = np.array([pos_finalJ[0],pos_finalJ[1],pos_finalJ[2]])
dist = LA.norm(dif_dist)
print(f"Diferencia con implementacion modelo Gepotencial = {round(dist/1000)} [m]")



    
    
    
    



