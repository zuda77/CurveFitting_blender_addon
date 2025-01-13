import bpy

bl_info = {
    "name": "Curve Fitting",
    "author": "zuda77",
    "version": (0, 1, 0),
    "blender": (3, 6, 0),
    "location": "Edit Mode > Vertex > Curve Fitting",
    "description": "Smooth out messy vertex arrangements while maintaining the original shape.",
    "warning": "",
    "tracker_url": "https://github.com/zuda77/CurveFitting_blender_addon/issues",
    "wiki_url": "https://github.com/zuda77/CurveFitting_blender_addon" ,
}

from . import curve_fitting 

def register():
    curve_fitting.register()


def unregister():
    curve_fitting.register()


if __name__ == "__main__":
    register()
