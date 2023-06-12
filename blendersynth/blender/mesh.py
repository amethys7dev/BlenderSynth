import os.path

import bpy
from .utils import GetNewObject
from .aov import AOV
import numpy as np

_primitives ={
	"cube": bpy.ops.mesh.primitive_cube_add,
	"sphere": bpy.ops.mesh.primitive_uv_sphere_add,
	"cylinder": bpy.ops.mesh.primitive_cylinder_add,
	"plane": bpy.ops.mesh.primitive_plane_add,
	"cone": bpy.ops.mesh.primitive_cone_add,
	"monkey": bpy.ops.mesh.primitive_monkey_add
}

class Mesh:
	def __init__(self, obj, material=None):
		self.obj = obj

		# Must have a material, create if not passed
		if material is None:
			material = bpy.data.materials.new(name='Material')
			material.use_nodes = True
		self.obj.data.materials.append(material)

	@classmethod
	def from_scene(cls, key):
		"""Create object from scene"""
		obj = bpy.data.objects[key]
		return cls(obj)

	@classmethod
	def from_primitive(cls, name='cube'):
		"""Create object from primitive"""
		assert name in _primitives, f"Primitive `{name}` not found. Options are: {list(_primitives.keys())}"

		importer = GetNewObject(bpy.context.scene)
		with importer:
			prim = _primitives[name]()  # Create primitive
		return cls(importer.imported_obj)  # Return object

	@classmethod
	def from_obj(cls, obj_loc):
		"""Load object from .obj file"""
		assert os.path.isfile(obj_loc) and obj_loc.endswith('.obj'), f"File `{obj_loc}` not a valid .obj file"

		directory, fname = os.path.split(obj_loc)

		importer = GetNewObject(bpy.context.scene)
		with importer:
			bpy.ops.import_scene.obj(filepath=fname, directory=directory, filter_image=True,
									 files=[{"name": fname}], forward_axis='X', up_axis='Z')

		return cls(importer.imported_obj)


	def get_all_vertices(self, ref_frame='WORLD'):
		verts = np.array([vert.co[:] + (1,) for vert in self.obj.data.vertices]).T

		if ref_frame == 'LOCAL':
			pass

		elif ref_frame == 'WORLD':
			world_matrix = np.array(self.obj.matrix_world)
			verts = np.dot(world_matrix, verts)

		else:
			raise ValueError(f"Invalid ref_frame: {ref_frame}. Must be one of ['LOCAL', 'WORLD']")

		verts = verts[:3, :] / verts[3, :]  # convert from homogeneous coordinates
		return verts.T


	@property
	def materials(self):
		return self.obj.data.materials

	def assign_pass_index(self, index: int):
		"""Assign pass index to object. This can be used when mask rendering."""
		self.obj.pass_index = index
		return index

	def assign_aov(self, aov: AOV):
		"""Assign AOV to object.
		Requires exactly 1 material on object."""
		assert len(self.materials) == 1, f"Object must have exactly 1 material. Found {len(self.materials)}"

		shader_node_tree = self.materials[0].node_tree
		assert shader_node_tree is not None, "Material must have a node tree"
		aov.add_to_shader(shader_node_tree)

	def set_euler_rotation(self, x, y, z):
		self.obj.rotation_euler = (x, y, z)

	def set_position(self, x, y, z):
		self.obj.location = (x, y, z)

	@property
	def bound_box(self):
		"""Return bounding box of object"""
		return self.obj.bound_box

	@property
	def matrix_world(self):
		"""Return world matrix of object"""
		return self.obj.matrix_world

	@property
	def scale(self):
		"""Return scale of object"""
		return self.obj.scale

	@scale.setter
	def scale(self, scale):
		"""Set scale of object"""
		self.obj.scale = scale

	@property
	def rotation_euler(self):
		"""Return euler rotation of object"""
		return self.obj.rotation_euler

	@rotation_euler.setter
	def rotation_euler(self, rotation):
		"""Set euler rotation of object"""
		self.obj.rotation_euler = rotation

	@property
	def location(self):
		"""Return location of object"""
		return self.obj.location

	@location.setter
	def location(self, location):
		"""Set location of object"""
		self.obj.location = location
