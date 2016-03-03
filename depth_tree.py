import os
import subprocess
from subprocess import call
source = '/home/prusso/gdrive/models/try'
for root, dirs, filenames in os.walk(source):
    for f in filenames:
	extension = os.path.splitext(f)[1]
	#import code
	#code.interact(local=locals())
	if extension == '.blend':
	        fullfilepath = os.path.abspath(os.path.join(root, f))
		callstring="blender"+" -b "+fullfilepath+" --python"+" img_one.py"+ " -- " + fullfilepath
		#import code
		#code.interact(local=locals())    	
		subprocess.call(callstring,shell=True)
