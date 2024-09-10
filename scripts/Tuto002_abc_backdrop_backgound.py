import bpy
import math
import random
import time
from mathutils import Euler, Color
from pathlib import Path



# function 1 --> random rotation
def randomly_rotate_object(obj_to_change):
    """ Applies a random rotation to an object
    """
    random_rot = (random.random()*2*math.pi, random.random()*2*math.pi, random.random()*2*math.pi)
    obj_to_change.rotation_euler = Euler(random_rot, 'XYZ')
    
    

# function 2 --> change color
def randomly_change_color(material_to_change):
    """ Changes the Principled BSDF Color of a material to random color
    """
    color = Color()
    hue = random.random() # random hue between 0 and 1
    color.hsv = (hue, 1, 1)
    rgba = [color.r, color.g, color.b, 1]
    material_to_change.node_tree.nodes['Principled BSDF'].inputs[0].default_value = rgba
    

"""
# e.g. change orientation and color
randomly_rotate_object(bpy.context.scene.objects['B'])
randomly_change_color(bpy.data.materials['Letter Material.001'])

# savet the image
bpy.context.scene.render.filepath = 'C:\\Users\\merwan.birem\\OneDrive - Flanders Make vzw\\Bureaublad\\test.png'
bpy.ops.render.render(write_still = True)
"""


output_path = Path('C:\\Users\\merwan.birem\\Downloads\\abc_test')


# objects names
obj_names = ['A', 'B', 'C']
obj_count = len(obj_names)

# Number of images to generate of each object for each split of the dataset
# Example
obj_renders_per_split = [('train', 300), ('val', 80), ('test', 10)]

# 
total_render_count = sum((obj_count*r[1] for r in obj_renders_per_split))

# Set all objects to be hidden in the render
for name in obj_names:
    bpy.context.scene.objects[name].hide_render = True
    
# Track teh starting image index for each object loop
start_idx = 0

# Keep track of start time (in secodns)
start_time = time.time()

# Loop through each split of the dataset
for split_name, renders_per_object in obj_renders_per_split:
    print(f'Starting split: {split_name} | Total renders: {renders_per_object * obj_count}') 
    print('===============================================')

    # Loop through the objects by name
    for obj_name in obj_names:
        print(f'Starting object: {split_name}/{obj_name}') 
        print('.............................................')
        
        # Get the next object and make it visible
        obj_to_render = bpy.context.scene.objects [obj_name] 
        obj_to_render.hide_render = False

        # Loop through all image renders for this object
        for i in range(start_idx, start_idx + renders_per_object): 
            # Change the object
            randomly_rotate_object(obj_to_render)
            randomly_change_color(obj_to_render.material_slots[0].material)

            # Log status
            print(f'Rendering image {i + 1} of {total_render_count}') 
            seconds_per_render = (time.time() - start_time) / (i + 1) 
            seconds_remaining  = seconds_per_render * (total_render_count - i - 1)
            print(f'Estimated time remaining: {time.strftime("%H:%M:%S", time.gmtime (seconds_remaining))}')

            # Update file path and render
            bpy.context.scene.render.filepath = str(output_path / split_name / obj_name / f'{str(i).zfill(6)}.png')
            bpy.ops.render.render(write_still=True)
            
        # Hide the object we are done with it
        obj_to_render.hide_render = True

        # Update the starting image index 
        start_idx += renders_per_object

# set all objects to be visible in rendering
for name in obj_names:
    bpy.context.scene.objects[name].hide_render = False