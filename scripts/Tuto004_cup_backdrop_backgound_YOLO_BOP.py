import bpy
import math
import random
import time
from mathutils import Euler, Color, Vector
from pathlib import Path
import json

def randomly_rotate_object(obj_to_change): 
    """Applies a random rotation to an object"""
    random_rot = (-math.pi/2, -math.pi, random.random() * 2 * math.pi)
    obj_to_change.rotation_euler = Euler(random_rot, 'XYZ')
    
def randomly_change_color(material_to_change):
    """Changes the Principled BSDF color of a material to a random color"""
    color = Color()
    hue = 0  # Random between .8 and .2
    saturation = 0  # Random between .2 and .8
    value = random.random() * .6
    color.hsv = (hue, saturation, value)
    rgba = [color.r, color.g, color.b, 1]
    material_to_change.node_tree.nodes["Principled BSDF"].inputs[0].default_value = rgba
    
def randomly_set_camera_position():
    """Randomly sets the camera position"""
    # Set the circular path position (0 to 100)
    bpy.context.scene.objects['CameraPathContainer'].constraints['Follow Path'].offset = random.random() * 100
    # Set the arc path position (0 to -100, not sure why, to be honest)
    bpy.context.scene.objects['CupPathContainer'].constraints['Follow Path'].offset_factor = random.random()

def get_bounding_box(obj_name):
    """Calculates 2D bounding box for YOLO format"""
    obj = bpy.data.objects[obj_name]
    bbox_corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    min_x = min(corner.x for corner in bbox_corners)
    max_x = max(corner.x for corner in bbox_corners)
    min_y = min(corner.y for corner in bbox_corners)
    max_y = max(corner.y for corner in bbox_corners)
    return (min_x, min_y, max_x, max_y)

def write_annotations(obj_name, image_path, annotations_path, class_id=0):
    """Writes YOLO and BOP annotations for the object"""
    scene = bpy.context.scene
    obj = bpy.data.objects[obj_name]

    # YOLO Annotation
    min_x, min_y, max_x, max_y = get_bounding_box(obj_name)
    x_center = (min_x + max_x) / 2 / scene.render.resolution_x
    y_center = (min_y + max_y) / 2 / scene.render.resolution_y
    width = (max_x - min_x) / scene.render.resolution_x
    height = (max_y - min_y) / scene.render.resolution_y

    yolo_annotation = f"{class_id} {x_center} {y_center} {width} {height}\n"
    
    with open(f"{annotations_path}/annotations.txt", "a") as yolo_file:
        yolo_file.write(yolo_annotation)

    # BOP Annotation
    translation = obj.location
    rotation = obj.rotation_euler.to_matrix().to_4x4()
    
    bop_annotation = {
        "scene_id": 1,
        "im_id": image_path.stem,
        "obj_id": class_id,
        "score": 1.0,
        "R": [list(row) for row in rotation],
        "t": [translation.x, translation.y, translation.z],
        "bounding_box": [min_x, min_y, max_x, max_y]
    }
    
    with open(f"{annotations_path}/bop_annotation.json", "a") as bop_file:
        json.dump(bop_annotation, bop_file, indent=4)
        bop_file.write('\n')

# Object names to render
cup_name = 'Cup'
cup_obj = bpy.context.scene.objects[cup_name]

obj_names = ['Cup']
obj_count = len(obj_names)

# Number of images to generate for each object for each split of the dataset
obj_renders_per_split = [('train', 3), ('val', 1)] 

# Output path
output_path = Path('C:\\Users\\merwan.birem\\Downloads\\cup_test')

# Set all objects to be hidden in rendering
for name in obj_names:
    if name != 'Empty':
        bpy.context.scene.objects[name].hide_render = True

# Tracks the starting image index for each object loop 
start_idx = 0

# Keep track of start time (in seconds) 
start_time = time.time()

# Loop through each split of the dataset
for split_name, renders_per_object in obj_renders_per_split:
    print(f'Starting split: {split_name} | Total renders: {renders_per_object * obj_count}') 
    print('===============================================================================')
    
    # Loop through the objects by name
    for obj_name in obj_names:
        print(f'Starting object: {split_name}/{obj_name}')
        print('...........................................')
        
        # Get the next object and make it visible
        if obj_name != 'Empty':
            obj_to_render = bpy.context.scene.objects[obj_name] 
            obj_to_render.hide_render = False
    
        # Loop through all image renders for this object
        for i in range(start_idx, start_idx + renders_per_object):
            # Change the object
            randomly_rotate_object(cup_obj)
            randomly_set_camera_position()
            randomly_change_color(obj_to_render.material_slots[0].material)
            
            # Log status
            print(f'Rendering image {i + 1} of {total_render_count}')
            seconds_per_render = (time.time() - start_time) / (i + 1)
            seconds_remaining = seconds_per_render * (total_render_count - i - 1)
            print(f'Estimated time remaining: {time.strftime("%H:%M:%S", time.gmtime(seconds_remaining))}')
            
            # Update file path and render
            img_path = output_path / split_name / obj_name / f"{str(i).zfill(6)}.png"
            bpy.context.scene.render.filepath = str(img_path)
            bpy.ops.render.render(write_still=True)
            
            # Write YOLO and BOP annotations
            annotations_path = output_path / split_name / obj_name
            annotations_path.mkdir(parents=True, exist_ok=True)
            write_annotations(obj_name, img_path, annotations_path)
            
            print(f"Annotations saved for image {img_path.name}")

    if obj_name != 'Empty':
        # Hide the object, we're done with it
        obj_to_render.hide_render = True
    
    # Update the starting image index 
    start_idx += renders_per_object

# Set all objects to be visible in rendering
for name in obj_names:
    if name != 'Empty':
        bpy.context.scene.objects[name].hide_render = False
