import ctypes as c
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import time
import datetime
import astropy.io.fits as pf
import cv2
import socket

def timenow():
    return int((datetime.datetime.now().timestamp()*1e3))

class image(c.Structure):
    _fields_ = [
        ('tnow',c.c_ulonglong),
        ('exposure',c.c_float),
        ('pixx',c.c_ushort),
        ('pixy',c.c_ushort),
        ('imgsize',c.c_uint),
        ('ccdtemp',c.c_int),
        ('boardtemp',c.c_int),
        ('chassistemp',c.c_int),
        ('picdata',1449072*c.c_ushort)
    ]

s = socket.socket()
print("Socket created successfully")
port = 12376
s.bind(('',port))
print("Socket bound to %s"%(port))
s.listen(5)
print("Socket is listening")

fig = plt.figure(figsize=(10,6))
fig.suptitle("Timestamp: %s, exposure: %f s\nCCD Temperature: %f"%(datetime.datetime.fromtimestamp(timenow()/1e3),0,0))
extent = 20,1260,110,950

im = plt.imshow(np.zeros((840,1240,3),dtype=np.uint8)+0xff,animated=True,extent=extent)

def animate(i):
    global s
    ct,addr = s.accept()
    print('Got connection from ', addr)
    val = ct.recv(c.sizeof(image))
    a = image()
    c.memmove(c.addressof(a),val,c.sizeof(image))
    ct.send('Data received'.encode('utf-8'))
    img = np.array(a.picdata[0:a.imgsize])
    data = np.reshape(img,(a.pixy,a.pixx))
    data = cv2.resize(data,dsize=(1392,1040),cv2.INTER_CUBIC)
    fig.suptitle("Timestamp: %s, exposure: %f s\nCCD Temperature: %f"%(datetime.datetime.fromtimestamp(timenow()/1e3),a.exposure,a.ccdtemp/100))
    x0 = 0 ; x1 = 1260
    xl = (x1 - x0)//4
    img = np.zeros((data[110:950,0:1260].shape[0],data[110:950,0:1260].shape[1],3),dtype=np.uint8)
    col = ((0x00,0xff,0x92),(0xff,0xe2,0x00),(0xaa,0x00,0x00),(0xff,0x00,0x00))
    for k in range(4):
	#plt.figure(figsize=(6,12))
        dat = np.zeros(data[110:950,x0+k*xl:x0+(k+1)*xl].shape,dtype=np.float64)
        dat += data[110:950,x0+k*xl:x0+(k+1)*xl]
        if True:
            dat = dat/65536.
            for z in range(3):
                img[:,x0+k*xl:x0+(k+1)*xl,z] += (dat*col[k][z]).astype(np.uint8)
			#plt.colorbar()
    im.set_array(img)
    return im,

animator = anim.FuncAnimation(fig,animate,blit=False,repeat=False)
plt.show()