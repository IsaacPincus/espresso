import espressomd
import espressomd.lb

from espressomd import lbboundaries
from espressomd import shapes
from espressomd import interactions

import object_in_fluid as oif
import numpy as np


boxX = 22.0
boxY = 14.0
boxZ = 14.0
system = espressomd.System(box_l=[boxX, boxY, boxZ])
system.cell_system.skin = 0.2
system.time_step = 0.1

# creating the template for RBCs
type = oif.OifCellType(nodes_file="input/rbc374nodes.dat", triangles_file="input/rbc374triangles.dat",
                        check_orientation=False, system=system, ks=0.005, kb=0.02, kal=0.007,
                        kag=0.9, kv=0.5, resize=[2.0, 2.0, 2.0], normal=True)

# creating the RBCs
cell = oif.OifCell(cell_type=type, particle_type=0, origin=[5.0, 5.0, 3.0])
cell1 = oif.OifCell(cell_type=type, particle_type=1, origin=[5.0, 5.0, 7.0], rotate=[0.0, np.pi/2, 0.0], particle_mass=0.5)

print("Cells created.")

boundaries = []

# bottom of the channel
tmp_shape = shapes.Rhomboid(corner=[0.0, 0.0, 0.0], a=[boxX, 0.0, 0.0], b=[0.0, boxY, 0.0], c=[0.0, 0.0, 1.0],
                          direction=1)
boundaries.append(tmp_shape)
oif.output_vtk_rhomboid(rhom_shape=tmp_shape, out_file="output/sim2/wallBottom.vtk")

# top of the channel
tmp_shape = shapes.Rhomboid(corner=[0.0, 0.0, boxZ-1], a=[boxX, 0.0, 0.0], b=[0.0, boxY, 0.0], c=[0.0, 0.0, 1.0],
                            direction=1)
boundaries.append(tmp_shape)
oif.output_vtk_rhomboid(rhom_shape=tmp_shape, out_file="output/sim2/wallTop.vtk")

# front wall of the channel
tmp_shape = shapes.Rhomboid(corner=[0.0, 0.0, 0.0], a=[boxX, 0.0, 0.0], b=[0.0, 1.0, 0.0], c=[0.0, 0.0, boxZ],
                            direction=1)
boundaries.append(tmp_shape)
oif.output_vtk_rhomboid(rhom_shape=tmp_shape, out_file="output/sim2/wallFront.vtk")

# back wall of the channel
tmp_shape = shapes.Rhomboid(corner=[0.0, boxY-1.0, 0.0], a=[boxX, 0.0, 0.0], b=[0.0, 1.0, 0.0], c=[0.0, 0.0, boxZ],
                            direction=1)
boundaries.append(tmp_shape)
oif.output_vtk_rhomboid(rhom_shape=tmp_shape, out_file="output/sim2/wallBack.vtk")

# obstacle - cylinder A
tmp_shape = shapes.Cylinder(center=[11.0, 2.0, 7.0], axis=[0.0, 0.0, 1.0], length=14.0, radius=2.0, direction=1)
boundaries.append(tmp_shape)
oif.output_vtk_cylinder(cyl_shape=tmp_shape, n=20, out_file="output/sim2/cylinderA.vtk")

# obstacle - cylinder B
tmp_shape = shapes.Cylinder(center=[16.0, 8.0, 7.0], axis=[0.0, 0.0, 1.0], length=14.0, radius=2.0, direction=1)
boundaries.append(tmp_shape)
oif.output_vtk_cylinder(cyl_shape=tmp_shape, n=20, out_file="output/sim2/cylinderB.vtk")

# obstacle - cylinder C
tmp_shape = shapes.Cylinder(center=[11.0, 12.0, 7.0], axis=[0.0, 0.0, 1.0], length=14.0, radius=2.0, direction=1)
boundaries.append(tmp_shape)
oif.output_vtk_cylinder(cyl_shape=tmp_shape, n=20, out_file="output/sim2/cylinderC.vtk")

for boundary in boundaries:
    system.lbboundaries.add(lbboundaries.LBBoundary(shape=boundary))
    system.constraints.add(shape=boundary, particle_type=10, penetrable=False)

print("Boundaries created.")

# cell-wall interactions
system.non_bonded_inter[0, 10].soft_sphere.set_params(a=0.0001, n=1.2, cutoff=0.1, offset=0.0)
system.non_bonded_inter[1, 10].soft_sphere.set_params(a=0.0001, n=1.2, cutoff=0.1, offset=0.0)

# cell-cell interactions
system.non_bonded_inter[0, 1].membrane_collision.set_params(a=0.0001, n=1.2, cutoff=0.1, offset=0.0)

print("Interactions created.")

# fluid
lb_params = {'agrid': 1, 'dens': 1, 'visc': 1.5, 'tau': system.time_step, 'ext_force_density': [0.00003, 0.0, 0.0]}
lbf = espressomd.lb.LBFluid(**lb_params)
system.actors.add(lbf)
system.thermostat.set_lb(LB_fluid=lbf, gamma=1.5)

# vtk_obs = ["density", "velocity_vector"]
# # create a VTK callback that automatically writes every 10 LB steps
# lb_vtk = espressomd.lb.VTKOutput(
#     identifier="lb_vtk_automatic", observables=vtk_obs, delta_N=10)
# lbf.add_vtk_writer(vtk=lb_vtk)

maxCycle = 100
# main integration loop
cell.output_vtk_pos_folded(file_name="output/sim2/cell_0.vtk")
cell1.output_vtk_pos_folded(file_name="output/sim2/cell1_0.vtk")
for i in range(1, maxCycle):
    system.integrator.run(steps=500)
    cell.output_vtk_pos_folded(file_name="output/sim2/cell_" + str(i) + ".vtk")
    cell1.output_vtk_pos_folded(file_name="output/sim2/cell1_" + str(i) + ".vtk")
    print("time: ", str(i*system.time_step*500))
    # print("cell volume: ", str(cell.mesh.volume()))
    # print("cell1 volume: ", str(cell1.mesh.volume()))
print("Simulation completed.")