import open3d as o3d
import numpy as np

mesh = o3d.io.read_triangle_mesh('RBC_6340_vertex_12676_face.ply')

vertices = np.asarray(mesh.vertices)
triangles = np.asarray(mesh.triangles)

with open('vertices.inp', 'w') as file:
    for index, vertex in enumerate(vertices):
        file.write(' '.join(map(str, vertex)) + ' \n')

with open('faces.inp', 'w') as file:
    for index, face in enumerate(triangles):
        file.write(' '.join(map(str, face)) + ' \n')

# def check_properties(name, mesh):
#     mesh.compute_vertex_normals()

#     edge_manifold = mesh.is_edge_manifold(allow_boundary_edges=True)
#     edge_manifold_boundary = mesh.is_edge_manifold(allow_boundary_edges=False)
#     vertex_manifold = mesh.is_vertex_manifold()
#     self_intersecting = mesh.is_self_intersecting()
#     watertight = mesh.is_watertight()
#     orientable = mesh.is_orientable()

#     print(name)
#     print(f"  edge_manifold:          {edge_manifold}")
#     print(f"  edge_manifold_boundary: {edge_manifold_boundary}")
#     print(f"  vertex_manifold:        {vertex_manifold}")
#     print(f"  self_intersecting:      {self_intersecting}")
#     print(f"  watertight:             {watertight}")
#     print(f"  orientable:             {orientable}")

#     geoms = [mesh]
#     if not edge_manifold:
#         edges = mesh.get_non_manifold_edges(allow_boundary_edges=True)
#     if not edge_manifold_boundary:
#         edges = mesh.get_non_manifold_edges(allow_boundary_edges=False)
#     if not vertex_manifold:
#         verts = np.asarray(mesh.get_non_manifold_vertices())
#         pcl = o3d.geometry.PointCloud(
#             points=o3d.utility.Vector3dVector(np.asarray(mesh.vertices)[verts]))
#         pcl.paint_uniform_color((0, 0, 1))
#         geoms.append(pcl)
#     if self_intersecting:
#         intersecting_triangles = np.asarray(
#             mesh.get_self_intersecting_triangles())
#         intersecting_triangles = intersecting_triangles[0:1]
#         intersecting_triangles = np.unique(intersecting_triangles)
#         print("  # visualize self-intersecting triangles")
#         triangles = np.asarray(mesh.triangles)[intersecting_triangles]
#         edges = [
#             np.vstack((triangles[:, i], triangles[:, j]))
#             for i, j in [(0, 1), (1, 2), (2, 0)]
#         ]
#         edges = np.hstack(edges).T
#         edges = o3d.utility.Vector2iVector(edges)
