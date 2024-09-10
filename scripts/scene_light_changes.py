import os

import bpy
from glob import glob
import random

# Source => 
# https://david-svitov.medium.com/generating-synthetic-data-step-by-step-in-blender-fefcb1954f01

texture_folder = '/home/david/Documents/textures'
images = glob(os.path.join(texture_folder, '*.*'))

save_folder = '/home/david/Documents/renders'
save_folder_hq = os.path.join(save_folder, 'HQ')
save_folder_lq = os.path.join(save_folder, 'LQ')
if not os.path.exists(save_folder_hq):
    os.makedirs(save_folder_hq)
if not os.path.exists(save_folder_lq):
    os.makedirs(save_folder_lq)

    
bpy.context.scene.render.resolution_x = 1280
bpy.context.scene.render.resolution_y = 1024

light = bpy.data.objects['Light']
plane = bpy.data.objects['Plane']

N_aug = 10

for num_texture, image_path in enumerate(images):
    bpy.data.images[-1].filepath = image_path
    
    for num_aug in range(N_aug):
        light.location[0] = random.uniform(-4, 4)
        light.location[1] = random.uniform(-3, 3)
        light.location[2] = random.uniform(1, 3)
        
        plane.rotation_euler[0] = random.uniform(-0.7, 0.7)
        plane.rotation_euler[1] = random.uniform(-0.1, 0.1)
        
        bpy.data.cameras['Camera'].dof.aperture_fstop = random.uniform(1.6, 2.8)
        
        filename = str(num_texture) + '_' + str(num_aug) + '.png'
    
        # Render to the file as LQ
        bpy.data.cameras['Camera'].dof.use_dof = True
        save_path = os.path.join(save_folder_lq, filename)
        bpy.context.scene.render.filepath = save_path
        bpy.ops.render.render(write_still = True)
        
        # Render to the file as HQ
        bpy.data.cameras['Camera'].dof.use_dof = False
        save_path = os.path.join(save_folder_hq, filename)
        bpy.context.scene.render.filepath = save_path
        bpy.ops.render.render(write_still = True)
