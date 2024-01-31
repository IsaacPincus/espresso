import open3d as o3d
import numpy as np

# 

# mesh = o3d.geometry.TriangleMesh.create_icosahedron()
# mesh = mesh.subdivide_loop(number_of_iterations=4)

mesh = o3d.io.read_triangle_mesh('sphere_4.ply')

# mesh = o3d.geometry.TriangleMesh.create_sphere()

print(mesh.get_center())
print(mesh.get_max_bound())
print(mesh.get_min_bound())

# mesh.scale(1.0/mesh.get_max_bound(), mesh.get_center())
# mesh.scale(D0/2/np.max(np.array(mesh.get_max_bound())), np.array(mesh.get_center()))

# # remap vertices to RBC
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

o3d.io.write_triangle_mesh('rbc_mesh.ply', mesh, write_ascii=True)

mesh.scale(16.0, np.array(mesh.get_center()))

vertices = np.asarray(mesh.vertices)
triangles = np.asarray(mesh.triangles)

l = 0.0
n = 0
for triangle in triangles:
    v0 = vertices[triangle[0]]
    v1 = vertices[triangle[1]]
    v2 = vertices[triangle[2]]
    l = l + np.linalg.norm(np.array(v0-v1)) + np.linalg.norm(np.array(v1-v2)) + np.linalg.norm(np.array(v0-v2))
    n = n + 3
print('avg length is: ' + str(l/n))

with open('vertices.inp', 'w') as file:
    for index, vertex in enumerate(vertices):
        file.write(' '.join(map(str, vertex)) + ' \n')

with open('faces.inp', 'w') as file:
    for index, face in enumerate(triangles):
        file.write(' '.join(map(str, face)) + ' \n')