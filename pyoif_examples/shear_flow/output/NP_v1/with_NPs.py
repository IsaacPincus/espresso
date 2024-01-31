import espressomd
import espressomd.lb

from espressomd import lbboundaries
from espressomd import shapes
from espressomd import interactions

import object_in_fluid as oif
import numpy as np

import sys
import shutil
import os

import matplotlib.pyplot as plt
import tqdm

def create_folder_and_copy_file(source_file, destination_folder):
    # Create the destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Combine the destination folder path with the source file name to get the full destination path
    destination_path = os.path.join(destination_folder, os.path.basename(source_file))

    try:
        # Copy the file to the destination folder
        shutil.copy(source_file, destination_path)
        print(f"File '{os.path.basename(source_file)}' copied to '{destination_folder}' successfully.")
    except Exception as e:
        print(f"Error: {e}")

# Example usage
source_file = "/home/ipincus/pyoip/espresso/pyoif_examples/shear_flow/with_NPs.py"
destination_folder = "/home/ipincus/pyoip/espresso/pyoif_examples/shear_flow/output/NP_v1/"

create_folder_and_copy_file(source_file, destination_folder)

# System constants
BOX_L = 30.0
TIME_STEP = 0.1

# fluid
AGRID = 0.5
VISCOSITY = 1.5
FORCE_DENSITY = [0.0, 0.0, 0.0]
DENSITY = 1.0
WALL_OFFSET = AGRID

system = espressomd.System(box_l=[BOX_L, 2*BOX_L, BOX_L])
system.time_step = TIME_STEP
system.cell_system.skin = 0.2

# creating the template for RBCs
# type = oif.OifCellType(nodes_file="input/rbc374nodes.dat", triangles_file="input/rbc374triangles.dat",
#                         check_orientation=False, system=system, ks=0.02, kb=0.016, kal=0.02,
#                         kag=0.9, kv=0.5, resize=[2.0, 2.0, 2.0])
# creating the template for RBCs
typeRBC = oif.OifCellType(nodes_file="input/rbc2562nodes_norm.dat", triangles_file="input/rbc2562triangles_norm.dat",
                        check_orientation=True, system=system, ks=0.008, kb=0.0004, kal=0.1,
                        kag=0.9, kv=0.5, resize=[16.0, 16.0, 16.0])

typeNP = oif.OifCellType(nodes_file="input/sphere304nodes.dat", triangles_file="input/sphere304triangles.dat",
                        check_orientation=False, system=system, ks=0.5, kb=0.3, kal=0.3,
                        kag=2.0, kv=1.5, resize=[2.0, 2.0, 2.0])

# creating the RBCs
cellRBC = oif.OifCell(cell_type=typeRBC, particle_type=0, origin=[15.0, 30.0, 15.0], rotate=[0.0, 0.0, 0.0])
cellRBC.output_vtk_pos_folded(file_name=os.path.join(destination_folder, "cell_0.vtk"))

suggested_gamma = cellRBC.suggest_LBgamma(VISCOSITY, DENSITY)
print("suggested RBC gamma is: ", str(suggested_gamma))

cellNP = oif.OifCell(cell_type=typeNP, particle_type=1, origin=[25.5, 30.0, 15.0], rotate=[0.0, 0.0, 0.0])
cellNP.output_vtk_pos_folded(file_name=os.path.join(destination_folder, "NP_s_0.vtk"))

cellNP_t = oif.OifCell(cell_type=typeNP, particle_type=1, origin=[15.0, 30.0, 18.5], rotate=[0.0, 0.0, 0.0])
cellNP_t.output_vtk_pos_folded(file_name=os.path.join(destination_folder, "NP_t_0.vtk"))

suggested_gamma = cellNP.suggest_LBgamma(VISCOSITY, DENSITY)
print("suggested NP gamma is: ", str(suggested_gamma))

lb_params = {'agrid': AGRID, 'dens': DENSITY, 'visc': VISCOSITY, 'tau': system.time_step, 'ext_force_density': FORCE_DENSITY}
lbf = espressomd.lb.LBFluid(**lb_params)
system.actors.add(lbf)
system.thermostat.set_lb(LB_fluid=lbf, gamma=suggested_gamma)


# interactions
EPSILON = 2e-4
CUTOFF = 1.3
SIGMA = 0.3
system.non_bonded_inter[0, 1].lennard_jones_cos.set_params(epsilon=EPSILON, cutoff=CUTOFF, sigma=SIGMA)
# EPS = 8e-4
# CUTOFF = 3.0
# ALPHA = 0.25
# RMIN = 0.04
# system.non_bonded_inter[0, 1].morse.set_params(eps=EPS, cutoff=CUTOFF, alpha=ALPHA, rmin=RMIN)

# main integration loop
steps = 500
maxCycle = 300
for i in range(1, maxCycle):
    system.integrator.run(steps=steps)
    time_str = str(round(i*system.time_step*steps))
    cellRBC.output_vtk_pos_folded(file_name=os.path.join(destination_folder, "cell_" + time_str + ".vtk"))
    cellNP.output_vtk_pos_folded(file_name=os.path.join(destination_folder, "NP_s_" + time_str + ".vtk"))
    cellNP_t.output_vtk_pos_folded(file_name=os.path.join(destination_folder, "NP_t_" + time_str + ".vtk"))
    print("time: ", str(i*system.time_step*steps))
    if i<30 and i % 5 == 0:
        CUTOFF = CUTOFF-0.1
        system.non_bonded_inter.reset()
        system.non_bonded_inter[0, 1].lennard_jones_cos.set_params(epsilon=EPSILON, cutoff=CUTOFF, sigma=SIGMA)
    if i==60:
        FLOW_VEL = 0.001
        top_wall = espressomd.shapes.Wall(normal=[1, 0, 0], dist=WALL_OFFSET)
        bottom_wall = espressomd.shapes.Wall(normal=[-1, 0, 0], dist=-(BOX_L - WALL_OFFSET))

        top_boundary = espressomd.lbboundaries.LBBoundary(shape=top_wall, velocity=[0.0,FLOW_VEL,0.0])
        bottom_boundary = espressomd.lbboundaries.LBBoundary(shape=bottom_wall, velocity=[0.0,-FLOW_VEL,0.0])

        system.lbboundaries.add(top_boundary)
        system.lbboundaries.add(bottom_boundary)

        print("Boundaries created.")

print("Simulation completed.")


