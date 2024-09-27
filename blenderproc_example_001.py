import blenderproc as bproc

# Initialize BlenderProc
bproc.init()

# Load the custom object (cup) into the scene
cup = bproc.loader.load_obj("C:\\software\\merwansky\\1.projects\\generate_synthetic_data_with_blender_tuto\\data\\uploads_files_635604_obj\\With Subdivisions\\Cup_3.obj")

# Create a simple plane as the ground
bproc.object.create_primitive('PLANE', scale=[2, 2, 1])

# Position the cup randomly on the plane
cup.set_location(bproc.sampler.rand_vec3(min=[-1, -1, 0], max=[1, 1, 0.5]))

# Rotate the cup randomly to add variety to the dataset
cup.set_rotation_euler(bproc.sampler.rand_vec3(min=[0, 0, 0], max=[3.14, 3.14, 3.14]))

# Set up random lighting in the scene
light = bproc.types.Light()
light.set_type("POINT")
light.set_location(bproc.sampler.rand_vec3(min=[-1, -1, 1], max=[1, 1, 3]))
light.set_energy(50)

# Render the scene and generate object detection annotations
data = bproc.renderer.render()

# Save the dataset and annotations for object detection
bproc.writer.write_coco_annotations("C:\\software\\merwansky\\1.projects\\generate_synthetic_data_with_blender_tuto\\data\\output_folder", instance_segm=False)