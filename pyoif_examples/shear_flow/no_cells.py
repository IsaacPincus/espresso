import espressomd
import espressomd.lb

from espressomd import lbboundaries
from espressomd import shapes
from espressomd import interactions

import object_in_fluid as oif
import numpy as np

import sys

import matplotlib.pyplot as plt
import tqdm

# System constants
BOX_L = 16.0
TIME_STEP = 0.1

system = espressomd.System(box_l=[BOX_L] * 3)
system.time_step = TIME_STEP
system.cell_system.skin = 0.2

# fluid
AGRID = 1.0
VISCOSITY = 1.5
FORCE_DENSITY = [0.0, 0.0, 0.0]
DENSITY = 1.0
WALL_OFFSET = AGRID
lb_params = {'agrid': AGRID, 'dens': DENSITY, 'visc': VISCOSITY, 'tau': system.time_step, 'ext_force_density': FORCE_DENSITY}
lbf = espressomd.lb.LBFluid(**lb_params)
system.actors.add(lbf)
# system.thermostat.set_lb(LB_fluid=lbf, gamma=1.5)

# # creating the template for RBCs
# type = oif.OifCellType(nodes_file="input/rbc374nodes.dat", triangles_file="input/rbc374triangles.dat",
#                         check_orientation=False, system=system, ks=0.02, kb=0.016, kal=0.02,
#                         kag=0.9, kv=0.5, resize=[2.0, 2.0, 2.0])

# # creating the RBCs
# cell = oif.OifCell(cell_type=type, particle_type=0, origin=[5.0, 5.0, 3.0])
# cell.output_vtk_pos_folded(file_name="output/sim1/cell_0.vtk")

FLOW_VEL = 0.1
top_wall = espressomd.shapes.Wall(normal=[1, 0, 0], dist=WALL_OFFSET)
bottom_wall = espressomd.shapes.Wall(normal=[-1, 0, 0], dist=-(BOX_L - WALL_OFFSET))

top_boundary = espressomd.lbboundaries.LBBoundary(shape=top_wall, velocity=[0.0,FLOW_VEL,0.0])
bottom_boundary = espressomd.lbboundaries.LBBoundary(shape=bottom_wall, velocity=[0.0,-FLOW_VEL,0.0])

system.lbboundaries.add(top_boundary)
system.lbboundaries.add(bottom_boundary)

print("Boundaries created.")

# main integration loop
maxCycle = 50
for i in range(1, maxCycle):
    system.integrator.run(steps=100)
    # print("time: ", str(i*system.time_step*100))
print("Simulation completed.")

print("shape is: " + str(lbf.shape[0]) + " y? " + str(lbf.shape[1]) + " z? " + str(lbf.shape[2]))
fluid_positions = (np.arange(lbf.shape[0]) + 0.5) * AGRID
# get all velocities as Numpy array and extract y components only
fluid_velocities = np.zeros((lbf.shape[0], lbf.shape[1], lbf.shape[2]))
for xx in range(lbf.shape[0]):
    for yy in range(lbf.shape[1]):
        for zz in range(lbf.shape[2]):
            fluid_velocities[xx,yy,zz] = (lbf[xx,yy,zz].velocity)[1]

# average velocities in y and z directions (perpendicular to the walls)
fluid_velocities = np.average(fluid_velocities, axis=(1,2))

print("max velocity is:", np.max(fluid_velocities))

fig1 = plt.figure(figsize=(10, 6))
# plt.plot(x_values, y_values, '-', linewidth=2, label='analytical')
plt.plot(fluid_positions, fluid_velocities, 'o', label='simulation')
plt.xlabel('Position on the $x$-axis', fontsize=16)
plt.ylabel('Fluid velocity in $y$-direction', fontsize=16)
plt.legend()
plt.show()