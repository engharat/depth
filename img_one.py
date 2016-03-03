#---------------------------------------------------
# File nodes.py
#---------------------------------------------------
import bpy
import mathutils
from math import *
import sys,random,time,os
from os.path import join
import os
debugg=0
argv = sys.argv
argv = argv[argv.index("--") + 1:]  # get all args after "--"
filepath=argv[0]
path=os.path.dirname(filepath)
file_name=bpy.path.display_name_from_filepath(filepath) #get the .blend name without extension and path
dirpath= join(path, file_name)
hdrpath= join(dirpath, 'HDR')
imgpath=join(dirpath, 'img')

category=path.split('/').pop()
#import code
#code.interact(local=locals())
if not os.path.exists(dirpath):
    os.makedirs(dirpath)
if not os.path.exists(hdrpath):
    os.makedirs(hdrpath)
if not os.path.exists(imgpath):
    os.makedirs(imgpath)
scene = bpy.context.scene
scene.use_nodes = True
nodes = scene.node_tree.nodes

#elapsed time
start_time = time.time()

#set scene unit to Metrics (centimeters!)
bpy.data.scenes["Scene"].unit_settings.system='METRIC'

#set scene resolution&engine:
scene.render.resolution_x = 256
scene.render.resolution_y = 256
scene.render.resolution_percentage = 100
bpy.data.scenes['Scene'].render.engine = 'CYCLES' # We use the Cycles Render

#set a new camera and its target:All meshes!
cam = bpy.data.cameras.new("Camera")
cam_ob = bpy.data.objects.new("Camera", cam)
bpy.context.scene.objects.link(cam_ob)
bpy.context.scene.camera = cam_ob
cam_ob.location=(2,0,5)
ob_target = bpy.data.objects.get('All Meshes', False)
track=bpy.data.objects["Camera"].constraints.new(type='TRACK_TO')
track.target=ob_target
track.up_axis = 'UP_Y'
track.track_axis='TRACK_NEGATIVE_Z'

#add a plane!
bpy.ops.mesh.primitive_plane_add()
ob2 = bpy.context.object
ob2.dimensions = (100,100,1)

#Use the default nodes generated in blender 
render_layers = nodes['Render Layers']
output_viewer = nodes['Composite']

#Add Map Value node for scaling and normalizing the Z values
norm = nodes.new('CompositorNodeNormalize')

#Add output DepthImg file node
output_file_Depthimg = nodes.new('CompositorNodeOutputFile')
output_file_Depthimg.base_path = imgpath

#Add output DepthEXR file node
output_file_DepthEXR = nodes.new('CompositorNodeOutputFile')
output_file_DepthEXR.base_path = hdrpath
output_file_DepthEXR.format.file_format='HDR'
scene.node_tree.links.new(
        render_layers.outputs['Z'],
        norm.inputs['Value']
    )
scene.node_tree.links.new(
        norm.outputs['Value'],
        output_file_Depthimg.inputs[0]
    )


#link the EXR node:
scene.node_tree.links.new(
        render_layers.outputs['Z'],
        output_file_DepthEXR.inputs[0]
    )

#camera center of rotation:
CoRX=0.0
CoRY=0.0
CoR=(CoRX,CoRY,0)
CamDist=2.2
jj=36
theta_out=radians(30)
phi_out=radians(jj*15)
cam_ob.location = (CoRX + CamDist*cos(phi_out)*sin(theta_out),CoRY+ CamDist*sin(phi_out)*sin(theta_out),CamDist*cos(theta_out))
output_file_DepthEXR.file_slots[0].path = category+'_'+file_name+'.hdr'
output_file_Depthimg.file_slots[0].path = category+'_'+file_name+'.png'							
bpy.ops.render.render(write_still=True, use_viewport=True)     
os._exit(0)
















#code for setting output filename:
#output_file_Depthimg.file_slots.remove(output_file_Depthimg.inputs[0])
# for i in range(0, 20):
#     idx = str(i + 1)
#     if i < 9:
#         idx = "0" + idx
#     output_file_Depthimg.file_slots.new("set_" + idx)

