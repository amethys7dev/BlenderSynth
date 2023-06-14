import blendersynth as bsyn
import numpy as np
bsyn.run_this_script(debug = False)  # If called from Python, this will run the current script in Blender
# If debug set to True, this will open Blender while running

comp = bsyn.Compositor()  # Create a new compositor - this manages all the render layers

# We create a simple scene with a random selection of objects on a plane
floor = bsyn.Mesh.from_primitive('plane', scale=20) # Create floor
N = 10 # Number of objects
R = 3 # Radius of circle
np.random.seed(6)
objects = []
for i in range(N):
	object = bsyn.Mesh.from_primitive(['monkey', 'cone', 'sphere', 'cube'][np.random.randint(4)],
							 scale=np.random.uniform(0.3, 1.0),
							 location=(np.sin(i / N * 2 * np.pi) * R, np.cos(i / N * 2 * np.pi) * R, 0) # place in a circle
									  )
	object.set_minimum_to('Z', 0)
	objects.append(object)

obj_pass_idx = objects[0].assign_pass_index(1)  # To show masking, we assign a pass index to the first object
point_light = bsyn.Light.create('POINT', location=(1, 0, 0), intensity=1000.)  # Create light object

# Set some render settings
bsyn.render.set_cycles_samples(10)
bsyn.render.set_resolution(512, 512)
camera = bsyn.Camera()

## RENDER PASSES
# Here we show several different rendering methods
bsyn.render.render_depth()  # Enable standard Blender depth pass
rgb_mask = comp.get_mask(obj_pass_idx, 'Image')  # create an RGB mask (i.e. only render monkey)
bounding_box_visual = comp.get_bounding_box_visual(objects)
bounding_box_visual.update(camera)

# AOV support - custom pass through a material shader
# For simplicity, we will assign all AOVs to all objects - but that doesn't have to be done.
all_objects = objects + [floor]

cam_normals_aov = bsyn.aov.NormalsAOV(ref_frame='CAMERA', polarity=[-1, 1, -1])
instancing_aov = bsyn.aov.InstanceRGBAOV()
class_aov = bsyn.aov.ClassRGBAOV()
UVAOV = bsyn.aov.UVAOV()  # UV Coordinates
NOCAOV = bsyn.aov.NOCAOV()  # Normalized Object Coordinates (NOC)

for aov in [cam_normals_aov, instancing_aov, class_aov, UVAOV, NOCAOV]:
	for obj in all_objects:
		obj.assign_aov(aov)

bsyn.world.set_color((0.2, 0.2, 0.6))

# Now we assign our render passes to the compositor, telling it what files to output
output_folder = 'quickstart'
comp.define_output('Image', output_folder, file_name='rgb', mode='image')  # render RGB layer (note mode='image')
comp.define_output(rgb_mask, output_folder, name='rgb_masked', mode='image') # render RGB layer masked by monkey
comp.define_output(bounding_box_visual, output_folder, name='bounding_box_visual', mode='image')
comp.define_output(instancing_aov, output_folder, name='instancing', mode='image')  # render instancing layer (note mode='image')
comp.define_output(class_aov, output_folder, name='semantic', mode='image')  # render class layer (note mode='image'

comp.define_output(cam_normals_aov, output_folder, name='normals', mode='data')  # render normals layer (note mode='data')
comp.define_output(UVAOV, output_folder, name='UV', mode='data')
comp.define_output(NOCAOV, output_folder, name='NOC', mode='data')
comp.define_output('Depth', output_folder, file_format='OPEN_EXR', mode='data')  # render depth as EXR (as not in 0-1 range)

comp.render()  # render all the different passes - see output folder for results