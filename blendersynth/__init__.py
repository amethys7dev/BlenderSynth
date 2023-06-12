from .run_this_script import run_this_script

# Import bpy attributes, only if bpy exists
import sys
from .utils.blender_locator import load_blender_path
if load_blender_path() == sys.argv[0]:  # if blender is running this script
	from bpy import *
	from .blender.mesh import Mesh
	from .blender import render
	from .blender.compositor.compositor import Compositor
	from .blender import aov
	from .file.dataset_inputs import INPUTS
	from . import file
	from .run.blender_interface import log_event
	from .blender import world
	from .blender.light import Light
	from .blender.camera import Camera
	from . import annotations

	# set render engine to cycles
	render.set_engine('CYCLES')

	# Clear default cube
	import bpy
	bpy.data.objects['Cube'].select_set(True)
	bpy.ops.object.delete()

else:
	# Imports for non blender
	from .run.run import execute_jobs
	from . import file
