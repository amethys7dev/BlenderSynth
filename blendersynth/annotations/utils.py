import bpy
from bpy_extras.object_utils import world_to_camera_view
import mathutils
import numpy as np


def project_point_to_image(P: mathutils.Vector, scene, camera):
	"""Return 2D (x, y) image coordinates of a 3D point P"""
	ndc_x, ndc_y, ndc_depth = world_to_camera_view(scene, camera, P)  # normalized device coords
	imgx = scene.render.resolution_x * ndc_x
	imgy = scene.render.resolution_y * (1 - ndc_y)  # ndc_y measured from bottom

	return imgx, imgy


def project_points(points, scene, camera):
	"""Project points to image plane.
	:param points: Nx3 matrix of points
	:param scene: bpy.types.Scene
	:param camera: bpy.types.Camera

	:return: Nx2 matrix of 2D image coordinates"""
	coords_2d = []
	for p in points:
		p_vec = mathutils.Vector(*(p,))
		coords_2d.append(project_point_to_image(p_vec, scene, camera))

	return np.array(coords_2d)
