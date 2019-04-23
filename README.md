# fly-demo
This repo contains a slightly modified [Panda3D Hello World](https://www.panda3d.org/manual/?title=A_Panda3D_Hello_World_Tutorial) with a basic implementation of mouselook and flying controls. The mouse will control the camera like an FPS, and the keyboard moves around in 3D space. The flymove.py script can be used in other projects to allow moving around a scene with more comfortable controls than the default mouse controls.

* WASD - normal FPS movement controls with respect to camera rotation
* Space - ascend
* Ctrl - descend

## FlyMove options

    FlyMove(base, mouse_magnitude=30, min_pitch=-60, max_pitch=60)

* showbase instance
* mouse_magnitude = multiplier for mouse sensitivity, higher is more sensitive (30 is default)
* min_pitch / max_pitch = lowest and highest angles from horizontal the mouse will be constrained. -90 and 90 will allow them to look directly up and down, -30 and 30 is 60 degrees of movement, 30 degrees above and below horizontal.
