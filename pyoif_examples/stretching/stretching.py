import espressomd
import espressomd.lb

from espressomd import lbboundaries
from espressomd import shapes
from espressomd import interactions

import object_in_fluid as oif
import numpy as np
import os, sys, time


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
    print ("force, simNo")
    print (" ")
else:
    force = float(sys.argv[1])
    simNo = sys.argv[2]

# GEOMETRY
boxX = 30.0
boxY = 10.0
boxZ = 20.0

# CELL
stretch = 3.91
noNodes = 374
originX = boxX/2
originY = boxY/2
originZ = boxZ/2
rbcMass = 100.0
partMass = rbcMass/noNodes
ks = 0.005
kb = 0.003
kal = 0.02
kag = 0.9
kv = 0.9
kvisc = 0.0

# for rings for stretching
# needs to be changed for different meshes
xBoundMinR = 0.9
xBoundMaxR = 0.98
xBoundMinL = 0.9
xBoundMaxL = 0.98

#  LBFLUID
grid = 1.0
dens = 1.0
visc = 1.5
surface = (np.sqrt(134.3)/3.91*stretch)**2
friction =(393.0/noNodes)*np.sqrt(surface/201.0619)*((5.6-1.82)/(5.853658537-1.5)*(visc-1.5)+(10-1.82)/(6-1.025)*(dens-1.025)+1.82)

# ITERATION PARAMETERS
timeStep = 0.05
counter = 0
noLoops = 200000
noSteps = 100        # how many steps in one stretching loop
noVtk = 100          # the cell vtk file written is written at (noVtk * noSteps)

accuracy = 0.001
previousL = -1.0
previousA = -1.0

# temp variables
tempVolume = 0.0    # we want to know the maximum deviation of volume and surface
tempSurface = 0.0
tempCycle = 0
cycle = 0

# INPUT FILES
fileNodes = "input/rbc" + str(noNodes) + "nodes.dat"
fileTriangles = "input/rbc" + str(noNodes) + "triangles.dat"

# OUTPUT FILES
dir = "output"
dirVtk = "output/vtk"
dirParam = "output/param"
dirVtkSimF = dirVtk+"/sim"+str(simNo)+"_"+str(force)+"vtk"
os.makedirs(dirVtkSimF)

#####################################
# initialization
######################################

system = espressomd.System(box_l=[boxX, boxY, boxZ])
system.time_step = timeStep
system.cell_system.skin = 0.2

# creating the template for cells
cellType = oif.OifCellType(nodes_file=fileNodes, triangles_file=fileTriangles, system = system, ks=ks, kb=kb, kal=kal, kag=kag, kv=kv, kvisc=kvisc,\
                       resize =[stretch,stretch,stretch])

# creating the RBC
cell = oif.OifCell(cell_type=cellType, particle_type=0, origin=[originX,originY,originZ], rotate=[np.pi/2.0, 0.0, 0.0], particle_mass=partMass)

# fluid
lb_params = {'agrid': grid, 'dens': dens, 'visc': visc, 'tau': timeStep}
lbf = espressomd.lb.LBFluid(**lb_params)
system.actors.add(lbf)
system.thermostat.set_lb(LB_fluid=lbf, gamma=friction)

# consider taking all nodes that have x coordinate approximately <5% or >95% total
rightStretchedParticles = list()
leftStretchedParticles = list()

for i in cell.mesh.points:
    posI = (i.get_pos()[0]-cell.get_origin()[0])/stretch
    if xBoundMaxR >= posI >= xBoundMinR:
        rightStretchedParticles.append(i)
    if -xBoundMinL >= posI >= -xBoundMaxL:
        leftStretchedParticles.append(i)

# we need to compute the contact size
# silica beads are touching the sphere in a circle
# we need to compute the diameter of this circle
# radius is computed as an average over yz-radius of points that are being pulled
radii = 0.0
for it in rightStretchedParticles:
    cy = it.get_pos()[1] - cell.get_origin()[1]
    cz = it.get_pos()[2] - cell.get_origin()[2]
    radii = radii + np.sqrt(cy**2 + cz**2)
rightContactDiameter = 2.0*radii/len(rightStretchedParticles)
print ("right diameter = " + str(rightContactDiameter))

radii = 0.0
for it in leftStretchedParticles:
    cy = it.get_pos()[1] - originY
    cz = it.get_pos()[2] - originZ
    radii = radii + np.sqrt(cy**2 + cz**2)

leftContactDiameter = 2.0*radii/len(leftStretchedParticles)
print ("left diameter = " + str(leftContactDiameter))

# check whether contact diameters are ok and
# check whether number of stretched points on the right is approximately the same as on the left
if rightContactDiameter > 2.2 or rightContactDiameter < 1.7:
    print ("wrong right diameter")
    foutParam.write("wrong right diameter")
    exit()
if leftContactDiameter > 2.2 or leftContactDiameter < 1.7:
    print ("wrong left diameter")
    foutParam.write("wrong left diameter")
    exit()

if abs(len(leftStretchedParticles)-len(rightStretchedParticles)) > 0.01 * noNodes:
    print ("numbers of particles stretched on right and left differ by more than 1% from nnode")
    foutParam.write("something is bad with particles:")
    foutParam.write("numbers of particles stretched on right and left differ by more than 1% from nnode")
    exit()

# applying force at two rings of particles
rightAppliedForce = force/len(rightStretchedParticles)
print ("force on one node on the right = " + str(rightAppliedForce))
leftAppliedForce = force/len(leftStretchedParticles)
print ("force on one node on the left = " + str(leftAppliedForce))

for it in rightStretchedParticles:
    it.set_force((rightAppliedForce, 0.0, 0.0))
for it in leftStretchedParticles:
    it.set_force((-leftAppliedForce, 0.0, 0.0))
print ("force has been applied to " + str(len(leftStretchedParticles)) + " particles on the left and " + str(len(rightStretchedParticles)) + " on the right side")

###################################################################
                       # MAIN SIMULATION
###################################################################

# save original surface, volume
originalVolume = cell.volume()
originalSurface = cell.surface()

stopSimulation = 0
cell.output_vtk_pos(dirVtkSimF+"/stretch_"+str(simNo)+"_vtk0.vtk")

###################################################################
                       # MAIN LOOP
###################################################################
while counter < noLoops:
    startTime = time.time()
    system.integrator.run(noSteps)
    counter += 1
    cycle = counter*noSteps

    # vtk file
    if counter % noVtk == 0:
        cell.output_vtk_pos(dirVtkSimF+"/stretch_"+str(simNo)+"_vtk"+str(cycle)+".vtk")

    # l-prologation should not be computed as maximal right coordinate minus maximal left coordinate
    # It should be computed from average of stretched particles
    rightX = 0
    for it in rightStretchedParticles:
        rightX = rightX + it.get_pos()[0]
    rightX = rightX / len(rightStretchedParticles)

    leftX = 0
    for it in leftStretchedParticles:
        leftX = leftX + it.get_pos()[0]
    leftX = leftX / len(leftStretchedParticles)

    length = rightX - leftX

    zMin = cell.pos_bounds()[4]
    zMax = cell.pos_bounds()[5]
    thickness = zMax - zMin

    # actual surface, volume and their deviation from originals
    volume = cell.volume()
    surface = cell.surface()
    devVolume = (volume - originalVolume)*100/originalVolume
    devSurface = (surface - originalSurface)*100/originalSurface

    if counter % noVtk == 0:
        fout = open(dirVtk+"/"+str(simNo)+"outDat.dat", "w")
        fout.write ("f l a l - previous_l previous_a - a devSurface devVolume ""\n")
        if abs(devSurface) > 3 or abs(devVolume) > 3:
            fout.write("Error: devSurface = "+str(devSurface)+", devVolume =  " +str(devVolume))
            stopSimulation = 1
        else:
            fout.write(str(force)+" "+str(length)+" "+str(thickness)+" "+str(length-previousL)+" "+str(previousA-thickness)+" "+str(devSurface)+" "+str(devVolume))
        fout.close()
        if (length-previousL)/previousL < 0.0001 and counter > 100:
            stopSimulation = 1
        previousA = thickness
        previousL = length

    # save the maximum of volume and surface deviation
    if abs(devVolume) > tempVolume:
        tempVolume = abs(devVolume)
        tempCycle = cycle

    if abs(devSurface) > tempSurface:
        tempSurface = abs(devSurface)
        tempCycle = cycle

    if stopSimulation == 1:
        counter = noLoops

# last vtk for this stretching
cell.output_vtk_pos(dirVtk+"/sim" + str(simNo) + "_force" + str(force) + ".vtk")
elapsedTime = time.time()-startTime
print ("Simulation completed in: " + str(elapsedTime))
foutFinalData = open(dir+'/sim'+str(simNo)+"_finalData.dat","a")
foutFinalData.write(str(force)+" "+str(length)+" "+str(thickness)+" "+str(volume)+" "+str(surface)+" "+str(cycle)+" "+str(tempVolume)+" "+str(tempSurface)+" "\
                    +str(tempCycle)+" "+str(time))