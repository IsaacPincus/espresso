import espressomd
import espressomd.lb

from espressomd import lbboundaries
from espressomd import shapes
from espressomd import interactions

import object_in_fluid as oif
import numpy as np

import os, sys, time, shutil

# this script is for stretching a cell according to Dao2006 optical tweezers experiment
# by applying a force at two opposite ends
# input: the stretching force
# it checks the transversal and axial cross-diameter
# stops when they stop changing (within prescribed accuracy)
# fluid is present and stationary

#####################################
# INPUT DATA
######################################

if len(sys.argv) != 3:
    print ("2 arguments expected, in this order")
    print ("LLSUB_RANK, LLSUB_SIZE")
    print (" ")
else:
    this_proc = int(sys.argv[1])
    no_proc = int(sys.argv[2])

simNo = this_proc
shear_vals = np.linspace(0, 2e-4, num=no_proc)
shear_rate = shear_vals[this_proc]


# GEOMETRY
boxX = 30.0
boxY = 60.0
boxZ = 30.0

# CELL
stretch = 16.0
noNodes = 2562
originX = boxX/2
originY = boxY/2
originZ = boxZ/2
rbcMass = 100.0
partMass = rbcMass/noNodes
ks = 0.003
kb = 0.0002
kal = 0.5
kag = 2.0
kv = 2.0
kvisc = 0.0
#  LBFLUID
grid = 1.0
dens = 1.0
visc = 1.5
# surface = (np.sqrt(134.3)/3.91*stretch)**2
# friction =(393.0/noNodes)*np.sqrt(surface/201.0619)*((5.6-1.82)/(5.853658537-1.5)*(visc-1.5)+(10-1.82)/(6-1.025)*(dens-1.025)+1.82)

# ITERATION PARAMETERS
TIME_STEP = 0.1
counter = 0
noLoops = 20000
noSteps = 100        # how many steps in one stretching loop
noVtk = 100          # the cell vtk file written is written at (noVtk * noSteps)

accuracy = 0.001
previousL = -1.0
previousA = -1.0

# fluid
AGRID = 1.0
VISCOSITY = 1.5
FORCE_DENSITY = [0.0, 0.0, 0.0]
DENSITY = 1.0
WALL_OFFSET = AGRID

# INPUT FILES
fileNodes = "input/rbc" + str(noNodes) + "nodes.dat"
fileTriangles = "input/rbc" + str(noNodes) + "triangles.dat"

# OUTPUT FILES
dir = "output"
dirVtk = "output/vtk"
dirParam = "output/param"
dirVtkSimF = dirVtk+"/sim"+str(simNo)+"_"+str(shear_rate)+"vtk"
os.makedirs(dirVtkSimF)

#####################################
# initialization
######################################

system = espressomd.System(box_l=[boxX, boxY, boxZ])
system.time_step = TIME_STEP
system.cell_system.skin = 0.2

# creating the template for RBCs
typeRBC = oif.OifCellType(nodes_file=fileNodes, triangles_file=fileTriangles, system = system, ks=ks, kb=kb, kal=kal, kag=kag, kv=kv, kvisc=kvisc,\
                       resize =[stretch,stretch,stretch])

# creating the RBCs
cellRBC = oif.OifCell(cell_type=typeRBC, particle_type=0, origin=[originX, originY, originZ], rotate=[0.0, 0.0, 0.0])
cellRBC.output_vtk_pos(dirVtkSimF+"/shear_"+str(simNo)+"_vtk0.vtk")

suggested_gamma = cellRBC.suggest_LBgamma(VISCOSITY, DENSITY)
print("suggested RBC gamma is: ", str(suggested_gamma))

# setting up LB parameters
lb_params = {'agrid': AGRID, 'dens': DENSITY, 'visc': VISCOSITY, 'tau': system.time_step, 'ext_force_density': FORCE_DENSITY}
lbf = espressomd.lb.LBFluid(**lb_params)
system.actors.add(lbf)
system.thermostat.set_lb(LB_fluid=lbf, gamma=suggested_gamma)

# boundaries and shear flow
FLOW_VEL = 0.5*boxX*shear_rate
top_wall = espressomd.shapes.Wall(normal=[1, 0, 0], dist=WALL_OFFSET)
bottom_wall = espressomd.shapes.Wall(normal=[-1, 0, 0], dist=-(boxX - WALL_OFFSET))

top_boundary = espressomd.lbboundaries.LBBoundary(shape=top_wall, velocity=[0.0,FLOW_VEL,0.0])
bottom_boundary = espressomd.lbboundaries.LBBoundary(shape=bottom_wall, velocity=[0.0,-FLOW_VEL,0.0])

system.lbboundaries.add(top_boundary)
system.lbboundaries.add(bottom_boundary)

print("Boundaries created.")

###################################################################
                       # MAIN LOOP
###################################################################
# save original surface, volume
originalVolume = cellRBC.volume()
originalSurface = cellRBC.surface()

stopSimulation = 0
cellRBC.output_vtk_pos(dirVtkSimF+"/shear_"+str(simNo)+"_vtk0.vtk")
startTime = time.time()
while counter < noLoops:
    system.integrator.run(noSteps)
    counter += 1
    cycle = counter*noSteps

    # get maximum sizes from gyration tensor
    S = np.zeros((3,3))
    noPoints = 0
    com = cellRBC.get_origin()
    for p in cellRBC.mesh.points:
        r = p.get_pos() - com
        S += np.outer(r, r)
        noPoints += 1
    S = S/noPoints
    # find eigenvectors and eigenvalues of gyration tensor, then sort
    (eigVals, eigVecs) = np.linalg.eig(S)
    index_array = np.argsort(eigVals)
    eigVecsSorted = eigVecs[index_array]
    eigVec0 = eigVecsSorted[:,0]
    eigVec1 = eigVecsSorted[:,1]
    eigVec2 = eigVecsSorted[:,2]
    # get lengths along each eigenvector
    max0 = -1000
    min0 = 1000
    max1 = -1000
    min1 = 1000
    max2 = -1000
    min2 = 1000
    for p in cellRBC.mesh.points:
        r = p.get_pos()
        # project r onto each eigenvector
        len0 = np.dot(r, eigVec0)
        len1 = np.dot(r, eigVec1)
        len2 = np.dot(r, eigVec2)
        # if it's largest or smallest, update
        if len0>max0:
            max0 = len0
        if len0<min0:
            min0 = len0
        if len1>max1:
            max1 = len1
        if len1<min1:
            min1 = len1
        if len2>max2:
            max2 = len2
        if len2<min2:
            min2 = len2
    rS0 = max0-min0
    rS1 = max1-min1
    rS2 = max2-min2

    # get maximum sizes in cartesian directions
    xMin = cellRBC.pos_bounds()[0]
    xMax = cellRBC.pos_bounds()[1]
    lenX = xMax - xMin
    yMin = cellRBC.pos_bounds()[2]
    yMax = cellRBC.pos_bounds()[3]
    lenY = yMax - yMin
    zMin = cellRBC.pos_bounds()[4]
    zMax = cellRBC.pos_bounds()[5]
    lenZ = zMax - zMin

    # actual surface, volume and their deviation from originals
    volume = cellRBC.volume()
    surface = cellRBC.surface()
    devVolume = (volume - originalVolume)*100/originalVolume
    devSurface = (surface - originalSurface)*100/originalSurface

    if counter % noVtk == 0:
        cellRBC.output_vtk_pos(dirVtkSimF+"/shear_"+str(simNo)+"_vtk"+str(cycle)+".vtk")
        print("cycle is: " + str(cycle) + ", max_stretch is: " + str(rS0))

        if abs(devSurface) > 3 or abs(devVolume) > 3:
            stopSimulation = 1
        # careful, this only works for tank-treading!
        if (rS0-previousL)/previousL < 0.001 and counter > 100:
            stopSimulation = 1
        previousL = rS0

    if stopSimulation == 1:
        counter = noLoops

# last vtk for this stretching
cellRBC.output_vtk_pos(dirVtk+"/sim" + str(simNo) + "_shear" + str(shear_rate) + ".vtk")
elapsedTime = time.time()-startTime
print ("Simulation completed in: " + str(elapsedTime))
foutFinalData = open(dir+'/sim'+str(simNo)+"_finalData.dat","a")
foutFinalData.write(str(shear_rate)+" "+str(rS0)+" "+str(rS1)+" "+str(rS2)+" "+str(lenX)+" "+str(lenY)+" "+str(lenZ)+" "+str(elapsedTime))