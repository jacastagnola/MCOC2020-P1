# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 16:05:34 2020

@author: Asus
"""
import xml
import xml.etree.ElementTree as ET
import numpy as np
import datetime as dt
from scipy.integrate import odeint
from scipy import special
import scipy as sc
import matplotlib.pyplot as plt

#from orbita_predicha import satelite
from time import perf_counter
#from implementacion_J2_J3 import satelite_Js

from sys import argv


# -----------------------------------------------------------------------------
# constants 
# -----------------------------------------------------------------------------
ncoef = 10

G = 6.67*(10**-11) # m^3/(kg*s^2)
M = 5.972*(10**24)
omega= 7.27*(10**-5)
horas=3600

# -----------------------------------------------------------------------------
# main 
# -----------------------------------------------------------------------------
def main():
    if(len(argv) == 1):
        eofname = "S1A_OPER_AUX_POEORB_OPOD_20200825T121215_V20200804T225942_20200806T005942.EOF"
    else:
        eofname = argv[1]
    
    data = np.transpose( leer_eof(eofname) )
    
    calc0 = odeint(fuerza, data[0,1:], data[:,0], args=(0,))
    #print( np.abs((data[-1,1:] - calc0[-1,:])/data[-1,1:]) )
     
    calc = odeint(fuerza, data[0,1:], data[:,0], args=(ncoef,))
    #print( np.abs((data[-1,1:] - calc[-1,:])/data[-1,1:]) )
    
    t1 = perf_counter()
    sol = odeint(fuerza, data[0,1:], data[:,0], args=(ncoef,))
    t2 = perf_counter()
    dt = t2 - t1 
    print (f"Para odeint se demoró: {dt}")
    

    
    diferencias = calc - calc0
    diferencias=np.array(diferencias)
    norma=np.sqrt(np.sum(diferencias[:,:3]**2,axis=1))
    sigmamax=round(norma[-1])
    
    print(f"deriva maxima {sigmamax} m")
    
    


# -----------------------------------------------------------------------------
# functions 
# -----------------------------------------------------------------------------
def fuerza(X, t, ncoef=ncoef, dx=1):
    """Calcula la fuerza que siente un cuerpo
    
    coef: coeficientes de Legendre
    """
    x, y, z = X[0], X[1], X[2]
    vx, vy, vz = X[3], X[4], X[5]
    
    c=np.cos(omega*t)
    s=np.sin(omega*t)
    
    R=np.array([[c,-s,0],
                [s,c,0],
                [0,0,1]])
    Rp=omega*np.array([[-s,-c,0],
                       [c,-s,0],
                       [0,0,0]])
    Rpp=(omega**2)*np.array([[-c,s,0],
                             [-s,-c,0],
                             [0,0,0]])
    
    # TODO: calcula la fuerza a partir del potencial.
    fx = 0.5 * (potencial(x+dx,y,z,ncoef) - potencial(x-dx,y,z,ncoef) ) / dx
    fy = 0.5 * (potencial(x,y+dx,z,ncoef) - potencial(x,y-dx,z,ncoef) ) / dx
    fz = 0.5 * (potencial(x,y,z+dx,ncoef) - potencial(x,y,z-dx,ncoef) ) / dx
    
    pos = np.array([x,y,z])
    vel = np.array([vx,vy,vz])
    
    f = np.array([fx, fy, fz]) - R.T@ (2*Rp @ vel + Rpp @ pos)

    return np.concatenate([[vx, vy, vz], f])


def potencial(x, y, z, ncoef=ncoef):     
    r = np.sqrt(x**2 + y**2 + z**2)
    theta = np.arctan2(z, np.sqrt(x**2 + y**2))
    phi = np.arctan2(y, x)
    
    # calcula el potencial
    P, dP = special.lpmn(ncoef+1,ncoef+1, np.sin(theta))
    
    
    u = 1 / r
    for n in range(1,ncoef):
        for m in range(n):
            u += P[m,n] * np.sin(m*phi) / r**(n+1)
            u += P[m,n] * np.cos(m*phi) / r**(n+1)
    
    return G*M * u
    

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

	t, x, y, z, vx, vy, vz = [np.zeros(count) for _ in range(7)]

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


# -----------------------------------------------------------------------------
# main 
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    main()