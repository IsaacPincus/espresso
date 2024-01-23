import espressomd
import espressomd.lb

import object_in_fluid as oif
import numpy as np

system = espressomd.System(box_l=[22.0, 14.0, 14.0])
system.time_step = 0.1
system.cell_system.skin = 0.2

# creating the template for RBCs
type = oif.OifCellType(nodes_file="input/rbc374nodes.dat", triangles_file="input/rbc374triangles.dat",
                        check_orientation=False, system=system, ks=0.02, kb=0.016, kal=0.02,
                        kag=0.9, kv=0.5, resize=[2.0, 2.0, 2.0])

# creating the RBCs
cell = oif.OifCell(cell_type=type, particle_type=0, origin=[5.0, 5.0, 3.0])
cell.output_vtk_pos_folded(file_name="output/sim1/cell_0.vtk")

# fluid
lb_params = {'agrid': 1, 'dens': 1, 'visc': 1.5, 'tau': system.time_step, 'ext_force_density': [0.0002, 0.0, 0.0]}
lbf = espressomd.lb.LBFluid(**lb_params)
system.actors.add(lbf)
system.thermostat.set_lb(LB_fluid=lbf, gamma=1.5)

# main integration loop
maxCycle = 100
for i in range(1, maxCycle):
    system.integrator.run(steps=100)
    cell.output_vtk_pos_folded(file_name="output/sim1/cell_" + str(i) + ".vtk")
    print("time: ", str(i*system.time_step*100))
print("Simulation completed.")