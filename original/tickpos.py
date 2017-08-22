from __future__ import print_function
import functools
import scipy 
import svgwrite

def getR1(r2,vRef,vOut):
    print(vOut)
    return r2/((vOut/vRef) - 1.0)

def getVOut(r1,r2,vRef):
    return vRef*(r2/r1 + 1.0)

# -----------------------------------------------------------------------------
r2 = 1.0e6
r1Min = 1.5e4
r1Max = 6.5e4 
vRef = 1.5 
vTickList =  [25, 30, 40,  50,  75, 100] 
angTickFudge =  [0,  -5, -25, -15, -25, -15]
angMin = 30.0
angMax = 330.0

x = 200
y = 200
r0 = 30 
r1 = 38 

# Print max and min values
vOutMax = getVOut(r1Min, r2, vRef)
vOutMin = getVOut(r1Max, r2, vRef)

r1TickMap = map(functools.partial(getR1,r2,vRef), vTickList)
r1TickList = [x for x in r1TickMap]
r1Range = [r1Min, r1Max]
angRange = [angMax, angMin]
angTickList = scipy.interp(r1TickList, r1Range, angRange)


print('vOutMin: {0}, vOutMax: {1}'.format(vOutMin, vOutMax))

dwg = svgwrite.Drawing('ticks.svg', profile='tiny')

angTickList = [x+y for x,y in zip(angTickList,angTickFudge)]

for ang in angTickList:
    x0 = x + r0*scipy.cos(ang*scipy.pi/180.0)
    y0 = y - r0*scipy.sin(ang*scipy.pi/180.0)
    x1 = x + r1*scipy.cos(ang*scipy.pi/180.0)
    y1 = y - r1*scipy.sin(ang*scipy.pi/180.0)
    dwg.add(dwg.line((x0, y0), (x1, y1), stroke=svgwrite.rgb(10, 10, 16, '%')))
dwg.save()





