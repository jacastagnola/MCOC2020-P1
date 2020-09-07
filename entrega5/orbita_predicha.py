import numpy as np

G=6.67*(10**-11) # m^3/(kg*s^2)
masa_tierra=5.972*(10**24)
omega= 7.27*(10**-5)
horas=3600

def satelite(z,t):
    
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
    zp=np.zeros(6)
    
    zp[0] = z[3]
    zp[1] = z[4]
    zp[2] = z[5]
    
    r_3=(np.sqrt(z[0]**2 + z[1]**2 + z[2]**2))**3
    
    z1 = z[0:3]
    z2 = z[3:6]
    
    zp[3:6] = -G*masa_tierra*z1/(r_3) - R.T@ (2*Rp @ z2 + Rpp @ z1)
    
    return zp

    print(zp)