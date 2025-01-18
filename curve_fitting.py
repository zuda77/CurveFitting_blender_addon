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

    bm.normal_update()
    obj.data.update()


###############################################################################################
def fit_vertices_to_surface(verts_coords, k, P, degree, border_weight_set=None):
##################################################################################################
    # Normalize the normal vector
    k /= np.linalg.norm(k)
    
    # Project vertices onto the plane defined by P and k
    projected_verts = [c - (np.dot(c - P, k) * k) for c in verts_coords]

    # Find the furthest projected vertex to determine basis vectors
    distances = [np.linalg.norm(p - P) for p in projected_verts]
    P_far = projected_verts[np.argmax(distances)]

    i = P_far - P
    i /= np.linalg.norm(i)
    j = np.cross(k, i)
    j /= np.linalg.norm(j)

    verts_ijk = [(np.dot(c - P, i), np.dot(c - P, j), np.dot(c - P, k)) for c in verts_coords]

    ij_coords = np.array([(v[0], v[1]) for v in verts_ijk])
    k_coords = np.array([v[2] for v in verts_ijk])

    # Construct matrix A for least squares fit
    A = np.column_stack([ij_coords[:, 0]**p * ij_coords[:, 1]**q for p in range(degree + 1) for q in range(degree + 1 - p)])

    # Apply weights if provided
    if border_weight_set is not None:
        weights = np.ones(len(k_coords))
        for idx, weight in border_weight_set.items():
            weights[idx] = weight
        A *= weights[:, None]
        k_coords *= weights

    try:
        coeffs, _, _, _ = np.linalg.lstsq(A, k_coords, rcond=None)
    except np.linalg.LinAlgError as e:
        raise ValueError(f"Least squares solution failed: {e}")

    def F(i, j):
        result = 0
        idx = 0
        for p in range(degree + 1):
            for q in range(degree + 1 - p):
                result += coeffs[idx] * (i**p) * (j**q)
                idx += 1
        return result

    fitting_verts = [(v[0], v[1], F(v[0], v[1])) for v in verts_ijk]
    fitting_verts_xyz = [P + v[0] * i + v[1] * j + v[2] * k for v in fitting_verts]

    return fitting_verts_xyz


def process_vertices_with_surface_fitting(context, curve_degree=4, border_weight=1, selected_faces=None):
    if selected_faces is None:
        print("Error: No selected faces provided for surface fitting.")
        return

    obj = bpy.context.object

    if obj is None or obj.type != 'MESH':
        print({'ERROR'}, "Please select a mesh object")
        return

    bm = bmesh.from_edit_mesh(obj.data)
    selected_verts = [v for v in bm.verts if v.select]
    if not selected_verts or len(selected_verts) < 3:
        print({'ERROR'}, "Please select at least 3 vertices")
        return

    # 境界エッジと境界頂点の検出
    selected_edges = [e for e in bm.edges if e.verts[0] in selected_verts and e.verts[1] in selected_verts]
    border_edges = [
        e for e in selected_edges
        if sum(1 for f in e.link_faces if f in selected_faces) == 1
    ]

    border_verts = set()
    for e in border_edges:
        border_verts.update(e.verts)

    # サーフェスフィッティング処理
    verts_coords = np.array([v.co for v in selected_verts])
    P_surf = np.mean(verts_coords, axis=0)
    face_normals = np.array([f.normal for f in selected_faces])
    normal_vec_surf = np.mean(face_normals, axis=0)
    normal_vec_surf /= np.linalg.norm(normal_vec_surf)

    border_weight_set = {selected_verts.index(v): border_weight for v in border_verts if v in selected_verts}

    try:
        fitting_verts_xyz = fit_vertices_to_surface(verts_coords, normal_vec_surf, P_surf, curve_degree, border_weight_set)

        for i, v in enumerate(selected_verts):
            v.co = fitting_verts_xyz[i]

        bmesh.update_edit_mesh(obj.data)
        bm.normal_update()
        obj.data.update()
    except Exception as e:
        print({'ERROR'}, f"Error during fitting: {e}")

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
        description="Curve weight factor for end points."
    )

    border_weight: bpy.props.IntProperty(
        name="Border Weight",
        default=1,
        min=1,
        max=1000,
        description="Surface weight factor for border points."
    )

    def execute(self, context):
        obj = context.object
        if obj is None or obj.type != 'MESH':
            self.report({'ERROR'}, "Please select a mesh object")
            return {'CANCELLED'}

        bm = bmesh.from_edit_mesh(obj.data)
        selected_verts = [v for v in bm.verts if v.select]
        if not selected_verts or len(selected_verts) < 3:
            self.report({'ERROR'}, "Please select at least 3 vertices")
            return {'CANCELLED'}

        selected_faces = {
            f for f in bm.faces 
            if all(v in selected_verts for v in f.verts)
        }

        if selected_faces:
            # 全ての頂点を含む面がある場合はsurface fitting
            process_vertices_with_surface_fitting(context, self.curve_degree, self.border_weight, selected_faces)
        else:
            # それ以外の場合はcurve fitting
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

