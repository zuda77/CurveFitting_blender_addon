import bpy


bl_info = {
    "name": "Curve Fitting Tool",
    "description": "Smooth out messy vertex arrangements while maintaining the original shape.",
    "author": "Your Name",
    "version": (1, 0, 0),
    "blender": (4, 2, 0),
    "location": "View3D > Edit Mesh > Context Menu",
    "category": "Mesh",
}

class AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    default_curve_degree: bpy.props.IntProperty(
        name="Default Curve Degree",
        default=4,
        min=1,
        max=20,
        description="Default degree of the polynomial fit for the curves."
    )

    default_ends_weight: bpy.props.IntProperty(
        name="Default Ends Weight",
        default=10,
        min=1,
        max=1000,
        description="Default weight factor for end points."
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="Default Settings for Curve Fitting Tool:")
        layout.prop(self, "default_curve_degree")
        layout.prop(self, "default_ends_weight")

from .curve_fitting import MESH_OT_process_vertices_with_curve_fitting

def register():
	bpy.utils.register_class(AddonPreferences)
	curve_fitting.register()

def unregister():
    curve_fitting.unregister()
    bpy.utils.unregister_class(AddonPreferences)
        
if __name__ == "__main__":
    register()
