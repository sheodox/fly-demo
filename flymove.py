from direct.showbase import DirectObject
from math import sin, cos, pi
from panda3d.core import WindowProperties, KeyboardButton


class FlyMove(DirectObject.DirectObject):
    def __init__(self, sb, mouse_magnitude=30, min_pitch=-60, max_pitch=60):
        self.base = sb
        self.mouse_magnitude = mouse_magnitude
        self.min_pitch = min_pitch
        self.max_pitch = max_pitch

        props = WindowProperties()
        props.set_cursor_hidden(True)
        props.set_mouse_mode(WindowProperties.MRelative)
        self.base.win.requestProperties(props)
        self.accept('mouse1', self.mouse1)

        tm = self.base.task_mgr
        tm.add(self.mouse_move, 'fp-mouse-move')
        tm.add(self.kb_move, 'fp-kb-move')
        self.keys = {
            'forward': KeyboardButton.ascii_key(b'w'),
            'left': KeyboardButton.ascii_key(b'a'),
            'right': KeyboardButton.ascii_key(b'd'),
            'backward': KeyboardButton.ascii_key(b's'),
            'up': KeyboardButton.space(),
            'down': KeyboardButton.control()
        }

    def kb_move(self, task):
        fwspeed = sidespeed = climb = 0
        is_down = self.base.mouseWatcherNode.is_button_down

        cam = self.base.camera

        if is_down(self.keys['forward']):
            fwspeed += 0.2

        if is_down(self.keys['left']):
            sidespeed -= 0.1

        if is_down(self.keys['right']):
            sidespeed += 0.1

        if is_down(self.keys['backward']):
            fwspeed -= 0.1

        if is_down(self.keys['down']):
            climb -= 0.1

        if is_down(self.keys['up']):
            climb += 0.1

        pos = cam.getPos()
        hpr = cam.getHpr()

        yawRad = hpr.x * (pi / 180)
        fwx = sin(yawRad) * fwspeed
        fwy = cos(yawRad) * fwspeed
        fwz = sin(hpr.y * (pi / 180)) * fwspeed
        swx = cos(yawRad) * sidespeed
        swy = sin(yawRad) * sidespeed

        cam.setPos(
            pos.x - fwx + swx,
            pos.y + fwy + swy,
            pos.z + fwz + climb
        )

        return task.cont

    def mouse_move(self, task):
        mw = self.base.mouseWatcherNode
        dx, dy = 0, 0
        if mw.hasMouse():
            dx, dy = mw.getMouseX(), mw.getMouseY()
            # recenter
            props = self.base.win.getProperties()
            self.base.win.movePointer(0, int(props.getXSize() / 2), int(props.getYSize() / 2))

        cam = self.base.camera
        hpr = cam.getHpr()
        cam.setHpr(
            hpr.x - self.mouse_magnitude * dx,
            max(self.min_pitch, min(self.max_pitch, hpr.y + self.mouse_magnitude * dy)),
            0
        )

        return task.cont

    def mouse1(self):
        print('mouse1')