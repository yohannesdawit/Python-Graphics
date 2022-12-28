#stormTrooperScene.py
#David Logan


from ren3d.scenedef import *

m = Material(*GOLD)
m.reflect = (.3,.3,.3)

g = Transformable(Box(color=Material((.3,.2,.4)))).scale(150,2,150)
#scene.add(g)

tp = Transformable(Mesh("stormTrooper.off", color=m,
                       smooth=True, recenter=True))
tp.scale(50,50,50).rotate_x(-90).rotate_y(-45).translate(0,0, -50)
scene.add(tp)

camera.set_perspective(60, 1.5, 80)
camera.set_view((0, 35, 210), (0,10,30), (0,1,0))

scene.set_light((-50, 100, 100), (1,1,1))
scene.ambient = (.5,.5,.5)
scene.background = (1,1,1)
scene.shadows = True
scene.reflections = 5

