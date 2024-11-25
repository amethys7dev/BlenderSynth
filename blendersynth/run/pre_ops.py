"""Some preferential blender operations to run (e.g. setup) that will be run before debug mode is entered"""
import bpy
from ..blender import render


def reset_scene():
    """Reset the scene to default settings"""
    bpy.ops.wm.read_factory_settings(use_empty=True)
    render.set_engine("CYCLES")


def on_script_open(delete_existing=True):
    """
    On script open:

    - Set Engine to CYCLES
    - Delete default Cube & Light
    - Disable splash screen
    """
    render.set_engine("CYCLES")

    if delete_existing:
        bpy.data.objects["Cube"].select_set(True)
        bpy.data.objects["Light"].select_set(True)
        bpy.ops.object.delete()

    bpy.context.preferences.view.show_splash = False  # disable splash screen
