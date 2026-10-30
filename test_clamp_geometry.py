# Test open alligator jaw clamping geometry
"""
In comp-specimen at translate(300, 205):
Object center is at y=55.
Object top is at y=45, bottom at y=65 (thickness 20px).

Left Clip:
Base/Boot at x=10..50, y=44..66 (centered at y=55).
Hinge at x=52, y=55.
Upper Jaw: slopes from (52, 50) to (80, 45) -> clamps onto top edge of object at y=45!
Lower Jaw: slopes from (52, 60) to (80, 65) -> clamps onto bottom edge of object at y=65!
Teeth along top jaw bite downward into y=45.
Teeth along bottom jaw bite upward into y=65.

Right Clip:
Base/Boot at x=190..230, y=44..66.
Hinge at x=188, y=55.
Upper Jaw: slopes from (188, 50) to (160, 45) -> clamps onto top edge of object at y=45!
Lower Jaw: slopes from (188, 60) to (160, 65) -> clamps onto bottom edge of object at y=65!
Teeth along top jaw bite downward into y=45.
Teeth along bottom jaw bite upward into y=65.

Object fits between x=80 and x=160!
"""
print('Clamping geometry calculated!')
