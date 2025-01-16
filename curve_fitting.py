import bpy
import bmesh
import numpy as np

# 頂点を処理する関数
def process_vertices_with_curve_fitting(context, curve_degree=4, ends_weight=10):
    obj = context.object
    if obj.mode != 'EDIT':
        bpy.ops.object.mode_set(mode='EDIT')

    bm = bmesh.from_edit_mesh(obj.data)
    selected_verts = [v for v in bm.verts if v.select]

    if not selected_verts or len(selected_verts) < 3:
        print("Insufficient vertices selected.")
        return

    edges = [e for e in bm.edges if e.verts[0].select and e.verts[1].select]

    if not edges:
        print("No connected edges found among selected vertices.")
        return

    ordered_verts = []
    edge_map = {}

    for e in edges:
        v1, v2 = e.verts
        edge_map.setdefault(v1.index, []).append(v2.index)
        edge_map.setdefault(v2.index, []).append(v1.index)

    start_vertex = None
    for vert in selected_verts:
        if len(edge_map.get(vert.index, [])) == 1:
            start_vertex = vert
            break

    if not start_vertex:
        print("Could not determine a starting vertex.")
        return

    current = start_vertex
    visited = set()

    while current and current.index not in visited:
        ordered_verts.append(current)
        visited.add(current.index)
        neighbors = edge_map.get(current.index, [])
        next_vertex = None
        for neighbor in neighbors:
            if neighbor not in visited:
                next_vertex = next((v for v in selected_verts if v.index == neighbor), None)
                if next_vertex:
                    current = next_vertex
                    break

    vecs = [ordered_verts[i+1].co - ordered_verts[i].co for i in range(len(ordered_verts) - 1)]

    coords = np.array([v.co[:] for v in ordered_verts])
    mean = np.mean(coords, axis=0)
    coords_centered = coords - mean
    covariance_matrix = np.cov(coords_centered.T)
    eigvals, eigvecs = np.linalg.eigh(covariance_matrix)
    principal_axes = eigvecs[:, ::-1]

    i_axis = principal_axes[:, 0]
    j_axis = principal_axes[:, 1]
    k_axis = principal_axes[:, 2]
    
    i_axis /= np.linalg.norm(i_axis)
    j_axis /= np.linalg.norm(j_axis)
    k_axis /= np.linalg.norm(k_axis)

    projected_vecs_i = np.dot(vecs, i_axis)
    projected_vecs_j = np.dot(vecs, j_axis)
    projected_vecs_k = np.dot(vecs, k_axis)

    if np.all(projected_vecs_i > 0) or np.all(projected_vecs_i < 0):
        principal_axes[:] = [i_axis, j_axis, k_axis]
    elif np.all(projected_vecs_j > 0) or np.all(projected_vecs_j < 0):
        principal_axes[:] = [j_axis, k_axis, i_axis]
    elif np.all(projected_vecs_k > 0) or np.all(projected_vecs_k < 0):
        principal_axes[:] = [k_axis, i_axis, j_axis]
    else:
        print("Could not find a monotonically increasing axis.")
        return
	
    transformed_coords = np.dot(coords_centered, principal_axes.T)
    
    min_proj_idx = np.argmin(transformed_coords[:, 0])
    max_proj_idx = np.argmax(transformed_coords[:, 0])

    def get_optimized_coeffs(x_data, y_data):
        weights = np.ones_like(x_data)
        weights[min_proj_idx] *= float(ends_weight)
        weights[max_proj_idx] *= float(ends_weight)

        A = np.vstack([x_data**i for i in range(curve_degree, -1, -1)]).T
        A_weighted = A * weights[:, np.newaxis]
        y_data_weighted = y_data * weights

        coeffs = np.linalg.inv(A_weighted.T @ A_weighted) @ A_weighted.T @ y_data_weighted
        return coeffs
        

    ij_coeffs = get_optimized_coeffs(transformed_coords[:, 0], transformed_coords[:, 1])
    ij_poly = np.poly1d(ij_coeffs)
    j1_coords = ij_poly(transformed_coords[:, 0])

    ik_coeffs = get_optimized_coeffs(transformed_coords[:, 0], transformed_coords[:, 2])
    ik_poly = np.poly1d(ik_coeffs)
    k1_coords = ik_poly(transformed_coords[:, 0])

    transformed_coords[:, 1] = j1_coords
    transformed_coords[:, 2] = k1_coords

    updated_coords = np.dot(transformed_coords, np.linalg.inv(principal_axes.T)) + mean

    for i, v in enumerate(ordered_verts):
        v.co = updated_coords[i]

    bmesh.update_edit_mesh(obj.data)

    print("Vertices processed and updated.")

# オペレータークラス
class MESH_OT_process_vertices_with_curve_fitting(bpy.types.Operator):
    bl_idname = "mesh.curve_fitting"
    bl_label = "Curve Fitting"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Smooth out uneven vertex arrangements"

    curve_degree: bpy.props.IntProperty(
        name="Curve Degree",
        default=4,
        min=1,
        max=20,
        description="Degree of the polynomial fit for the curves."
    )

    ends_weight: bpy.props.IntProperty(
        name="Ends Weight",
        default=10,
        min=1,
        max=1000,
        description="Weight factor for end points."
    )

    def execute(self, context):
        process_vertices_with_curve_fitting(context, self.curve_degree, self.ends_weight)
        return {'FINISHED'}

# メニューにオペレーターを追加する関数
def menu_func(self, context):
    self.layout.operator(MESH_OT_process_vertices_with_curve_fitting.bl_idname)

# 登録
def register():
    bpy.utils.register_class(MESH_OT_process_vertices_with_curve_fitting)
    bpy.types.VIEW3D_MT_edit_mesh_vertices.append(menu_func)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.prepend(menu_func)  # prependで先頭に追加

# 解除
def unregister():
    bpy.utils.unregister_class(MESH_OT_process_vertices_with_curve_fitting)
    bpy.types.VIEW3D_MT_edit_mesh_vertices.remove(menu_func)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(menu_func)  # 削除

