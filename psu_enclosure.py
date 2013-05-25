"""
Creates an enclosure
"""
from py2scad import *

INCH2MM = 25.4

# Inside dimensions
x,y,z = (3.345 + 2*0.25 + 0.25)*INCH2MM, (2.1 + 0.15)*INCH2MM, 1.0*INCH2MM
hole_list = []

dc_jack_hole = {
        'panel': 'front',
        'type': 'round',
        'location': (-1.072*INCH2MM,0.573*INCH2MM-0.5*z), 
        'size' : 0.42*INCH2MM
        }
hole_list.append(dc_jack_hole)

switch_hole = {
        'panel' : 'front',
        'type' : 'rounded_square',
        'location': (-0.294*INCH2MM, 0.623*INCH2MM - 0.5*z),
        'size': (0.752*INCH2MM,0.3*INCH2MM,1)
        }
hole_list.append(switch_hole)

pos_neg_hole = {
        'panel' : 'front',
        'type': 'rounded_square',
        'location': (0.988*INCH2MM, 0.623*INCH2MM - 0.5*z),
        'size' : (0.9*INCH2MM, 0.45*INCH2MM,1),
        }
hole_list.append(pos_neg_hole)

mount_x = 3.15*INCH2MM
mount_y = 1.90*INCH2MM
mount_diam = 0.1160*INCH2MM
for i in (-1,1):
    for j in (-1,1):
        pos_x = 0.5*mount_x*i
        pos_y = 0.5*mount_y*j
        hole = {
                'panel': 'bottom',
                'type': 'round',
                'location': (pos_x,pos_y),
                'size': mount_diam
                }
        hole_list.append(hole)


pot_hole = {
        'panel': 'top',
        'type': 'round',
        'location': (1.11*INCH2MM, 0.578*INCH2MM),
        'size': 0.55*INCH2MM,
        }
hole_list.append(pot_hole)


params = {
        'inner_dimensions'        : (x,y,z), 
        'wall_thickness'          : 3.0, 
        'lid_radius'              : 0.1*INCH2MM,  
        'top_x_overhang'          : 0.1*INCH2MM,
        'top_y_overhang'          : 0.1*INCH2MM,
        'bottom_x_overhang'       : 0.1*INCH2MM,
        'bottom_y_overhang'       : 0.1*INCH2MM, 
        'lid2front_tabs'          : (0.2,0.5,0.8),
        'lid2side_tabs'           : (0.25, 0.75),
        'side2side_tabs'          : (0.5,),
        'lid2front_tab_width'     : 0.75*INCH2MM,
        'lid2side_tab_width'      : 0.75*INCH2MM, 
        'side2side_tab_width'     : 0.5*INCH2MM,
        'standoff_diameter'       : 0.25*INCH2MM,
        'standoff_offset'         : 0.05*INCH2MM,
        'standoff_hole_diameter'  : 0.116*INCH2MM, 
        'hole_list'               : hole_list,
        }

enclosure = Basic_Enclosure(params)
enclosure.make()

part_assembly = enclosure.get_assembly(
        explode=(0,0,0),
        show_front=True,
        show_top=True,
        show_standoffs=True,
        )
part_projection = enclosure.get_projection()

prog_assembly = SCAD_Prog()
prog_assembly.fn = 50
prog_assembly.add(part_assembly)
prog_assembly.write('enclosure_assembly.scad')

prog_projection = SCAD_Prog()
prog_projection.fn = 50
prog_projection.add(part_projection)
prog_projection.write('enclosure_projection.scad')
