import pymeshlab as ml
import open3d as o3d
import numpy as np

ms = ml.MeshSet()
# ms.load_new_mesh('rbc_mesh.ply')
# ml.print_filter_list()

# create a sphere throught subdivision of an icosahedron
# ms.apply_filter('Sphere', radius=1.0, subdiv=4)
ms.create_sphere(radius=1,subdiv=4)
ms.apply_filter('compute_matrix_from_scaling_or_normalization',
                scalecenter='origin', unitflag=True)

# save mesh, we will then load and alter it in o3d
ms.save_current_mesh('sphere.ply')

# read into o3d, move vertices, then send back to meshlab
mesh = o3d.io.read_triangle_mesh('sphere.ply')
D0 = 1+1e-7
a0 = 0.0518
a1 = 2.0026
a2 = -4.491
for vertex in np.asarray(mesh.vertices):
    x = vertex[0]
    y = vertex[1]
    z = vertex[2]
    if z>0:
        vertex[2] = D0*np.sqrt(1-4*(x*x+y*y)/(D0*D0))*(a0 + a1*(x*x+y*y)/(D0*D0) + a2*(x*x+y*y)**2/(D0**4))
    else:
        vertex[2] = -D0*np.sqrt(1-4*(x*x+y*y)/(D0*D0))*(a0 + a1*(x*x+y*y)/(D0*D0) + a2*(x*x+y*y)**2/(D0**4))
    # print("vertex x y z is: " + str(vertex))
        
o3d.io.write_triangle_mesh('rbc.ply', mesh, write_ascii=True)

# overwrite ms, then read back in
ms = ml.MeshSet()
ms.load_new_mesh('rbc.ply')
#apply explicit remeshing, which cleans up the face sizes
ms.apply_filter('meshing_isotropic_explicit_remeshing',
                iterations=500, adaptive=True, splitflag=False,
                collapseflag=False)

# write out the final mesh
ms.save_current_mesh('rbc.ply')

# read back into o3d (yeah I know lol) and write out as faces and vertices
mesh = o3d.io.read_triangle_mesh('rbc.ply')

vertices = np.asarray(mesh.vertices)
triangles = np.asarray(mesh.triangles)

with open('vertices.inp', 'w') as file:
    for index, vertex in enumerate(vertices):
        file.write(' '.join(map(str, vertex)) + ' \n')

with open('faces.inp', 'w') as file:
    for index, face in enumerate(triangles):
        file.write(' '.join(map(str, face)) + ' \n')