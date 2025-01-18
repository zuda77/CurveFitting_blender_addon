import bpy


bl_info = {
    "name": "Curve Fitting",
    "description": "Smooth out uneven vertex arrangements on the curve",
    "author": "zuda77",
    "version": (0, 3, 0),
    "blender": (4, 2, 0),
    "location": "View3D > Edit Mesh > Context Menu",
    "category": "Mesh",
}

class AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

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

    def draw(self, context):
        layout = self.layout
        layout.label(text="Default Settings for Curve Fitting:")
        layout.prop(self, "curve_degree")
        layout.prop(self, "ends_weight")
        layout.prop(self, "border_weight")

from .curve_fitting import MESH_OT_process_vertices_with_curve_fitting

def register():
	bpy.utils.register_class(AddonPreferences)
	curve_fitting.register()

def unregister():
    curve_fitting.unregister()
    bpy.utils.unregister_class(AddonPreferences)
        
if __name__ == "__main__":
    register()
