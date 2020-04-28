from math import pi,cos,sin
import numpy as np


def estimate_3D_to_2D(ox,oy,FocalLength_x,FocalLength_y,a,b,g,x_trans,z_trans,r,points):

	r_x = [[1,0,0],[0,cos(a),-sin(a)],[0,sin(a),cos(a)]]
	r_y = [[cos(b),0,sin(b)],[0,1,0],[-sin(b),0,cos(b)]]
	r_z = [[cos(g),-sin(g),0],[sin(g),cos(g),0],[0,0,1]]

	bag = np.matmul (np.matmul (r_y, r_x),r_z)

	rm = bag

	xx = np.array([rm[0,0], rm[1,0], rm[2,0]])
	yy = np.array([rm[0,1], rm[1,1], rm[2,1]])
	zz = np.array([rm[0,2], rm[1,2], rm[2,2]])



	x = r*-zz[0]
	y = r*-zz[1]
	z = r*-zz[2]

	pos = np.array([x,y,z])+x_trans*xx+z_trans*yy

	worldOrientation = rm.T
	worldLocation = pos*1000

	rotationMatrix = worldOrientation.T
	translationVector = -np.matmul(worldLocation,worldOrientation.T)

	a = np.matmul(points,rotationMatrix)+np.tile(translationVector,[np.size(points,0),1])

	u =  ox-FocalLength_x*a[:,0]/a[:,2]
	v =  oy-FocalLength_y*a[:,1]/a[:,2]

	results = np.array([u,v]).T

	return results


spe_points = [ [-37.5,	16,	-36.5], 
				[-36.5,	16,	-37.5],
				[-37.5,	0,	-36.5],
				[-36.5,	0,	-37.5],
				[36.5,	16,	-37.5],
				[37.5,	16,	-36.5],
				[36.5,	0,	-37.5],
				[37.5,	0,	-36.5],
				[-37.5,	16,	-22.5],
				[-36.5,	16,	-21.5],
				[-37.5,	0,	-22.5],
				[-36.5,	0,	-21.5],
				[37.5,	16,	-22.5],
				[36.5,	16,	-21.5],
				[37.5,	0,	-22.5],
				[36.5,	0,	-21.5],
				[-15,	9,	35.5],
				[-15,	0,	35.5],
				[15,	9,	35.5],
				[15, 	0,	35.5],
				[-13,	9,	37.5],
				[-13,	0,	37.5],
				[13,	9,	37.5],
				[13,	0,	37.5],
				[15,	16,	-9.5],
				[13,	16,	-7.5],
				[-15,	16,	-9.5],
				[-13,	16,	-7.5]]

ox = 3.245938552764519e+02
oy = 2.634932055129686e+02
FocalLength_x = 5.938737905768464e+02
FocalLength_y = 5.939301207515520e+02

x1 = 160
x2 = 640
y1 = 0
y2 = 480

a_ran = [pi/3.,pi/2.] 
a_intev = 15
b_ran = [pi,pi/2.*3.]
b_intev = 45
g_ran = [-pi/16.,pi/16.]
g_intev = 5
x_ran = [0.005,0.025]
x_intev = 20
z_ran = [-0.025,0.005]
z_intev = 30
r_ran = [0.135,0.155]
r_intev = 20




y = np.zeros((a_intev*b_intev*g_intev*x_intev*z_intev*r_intev, 6))
index = 0
all_index = 0

for a in range(a_intev):
	a_ = a_ran[0]+(a_ran[1]-a_ran[0])/a_intev*a
	for b in range(b_intev):
		b_ = b_ran[0]+(b_ran[1]-b_ran[0])/b_intev*b
		for g in range(g_intev):
			g_ = g_ran[0]+(g_ran[1]-g_ran[0])/g_intev*g
			for x in range(x_intev):
				x_ = x_ran[0]+(x_ran[1]-x_ran[0])/x_intev*x
				for z in range(z_intev):
					z_ = z_ran[0]+(z_ran[1]-z_ran[0])/z_intev*z
					for r in range(r_intev):
						r_ = r_ran[0]+(r_ran[1]-r_ran[0])/r_intev*r

						spe_points2D = estimate_3D_to_2D(ox,oy,FocalLength_x,FocalLength_y,\
						a_,b_,g_,x_,z_,r_,spe_points)

						if_window_in = True

						for k in range(np.size(spe_points2D,0)):
							u = spe_points2D[k,0]
							v = spe_points2D[k,1]

							if u<x1 or u>=x2 or v<y1 or v>=y2:
								if_window_in = False
								break

						if if_window_in==True:
							y[index,:]=[a_,b_,g_,x_,z_,r_]
							index = index+1

						all_index = all_index+1

						print('all:{}/{} in:{}'.format(all_index,a_intev*b_intev*g_intev*x_intev*z_intev*r_intev,index))

np.save('pose(122302,122312)',y[:index+1,:])

