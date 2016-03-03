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
#import code
#code.interact(local=locals())
if  bpy.data.objects.get('All Meshes') is None:
    with open("errors.txt", "a+") as f:
        str1=filepath+'\n'
        f.write(str1)
        f.close()
os._exit(0)
