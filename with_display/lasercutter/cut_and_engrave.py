import os
import sys
from py2gcode import gcode_cmd
from py2gcode import cnc_laser

dxfFileName = sys.argv[1]

numLayer = 8 
#engraveLayerList = ['engrave{0}'.format(i) for i in range(numLayer)]
#vectorLayerList = ['vector{0}'.format(i) for i in range(numLayer)]

engraveLayerList = ['engrave',]
vectorLayerList = ['vector', ]

# Create full 24x24 cuting layout
prog = gcode_cmd.GCodeProg()
prog.add(gcode_cmd.GenericStart())
prog.add(gcode_cmd.Space())

if len(vectorLayerList) > 1:
    # Etching
    param = {
            'fileName'    :  dxfFileName,
            'layers'      :  engraveLayerList,
            'dxfTypes'    :  ['LINE','ARC'],
            'laserPower'  :  350,
            'feedRate'    :  60,
            'convertArcs' :  True,
            'startCond'   : 'minX',
            'direction'   : 'ccw',
            'ptEquivTol'  :  0.4e-3,
            }
    
    vectorEtch = cnc_laser.VectorCut(param)
    prog.add(vectorEtch)
    
    # Cutting
    param = {
            'fileName'    :  dxfFileName,
            'layers'      :  vectorLayerList,
            'dxfTypes'    :  ['LINE','ARC','CIRCLE'],
            'laserPower'  :  600,
            'feedRate'    :  25,
            'convertArcs' :  True,
            'startCond'   : 'minX',
            'direction'   : 'ccw',
            'ptEquivTol'  :  0.4e-3,
            }
    
    vectorCut = cnc_laser.VectorCut(param)
    prog.add(vectorCut)
    
    prog.add(gcode_cmd.Space())
    prog.add(gcode_cmd.End(),comment=True)
    
    baseName, ext = os.path.splitext(dxfFileName)
    ngcFileName = '{0}.ngc'.format(baseName)
    prog.write(ngcFileName)


# Create individual cutting files for each set of layer numbers
for engraveLayer, vectorLayer in zip(engraveLayerList,vectorLayerList):

    prog = gcode_cmd.GCodeProg()
    prog.add(gcode_cmd.GenericStart())
    prog.add(gcode_cmd.Space())
    
    # Etching
    param = {
            'fileName'    :  dxfFileName,
            'layers'      :  [engraveLayer],
            'dxfTypes'    :  ['LINE','ARC'],
            'laserPower'  :  350,
            'feedRate'    :  60,
            'convertArcs' :  True,
            'startCond'   : 'minX',
            'direction'   : 'ccw',
            'ptEquivTol'  :  0.4e-3,
            }
    
    vectorEtch = cnc_laser.VectorCut(param)
    prog.add(vectorEtch)

    print(vectorLayer)
    
    # Cutting
    param = {
            'fileName'    :  dxfFileName,
            'layers'      :  [vectorLayer],
            'dxfTypes'    :  ['LINE','ARC','CIRCLE'],
            'laserPower'  :  600,
            'feedRate'    :  25,
            'convertArcs' :  True,
            'startCond'   : 'minX',
            'direction'   : 'ccw',
            'ptEquivTol'  :  0.4e-3,
            }
    
    vectorCut = cnc_laser.VectorCut(param)
    prog.add(vectorCut)
    
    prog.add(gcode_cmd.Space())
    prog.add(gcode_cmd.End(),comment=True)
    
    baseName, ext = os.path.splitext(dxfFileName)
    ngcFileName = '{0}_{1}.ngc'.format(baseName,vectorLayer)
    prog.write(ngcFileName)
