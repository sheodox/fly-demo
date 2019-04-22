from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase, NodePath, loadPrcFile, PointLight, AmbientLight, VBase4, DirectionalLight
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3, loadPrcFileData, Material, Fog
from flymove import FlyMove

loadPrcFileData('', 'win-size 1440 900')


class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.camera.setPos(0, 0, 3)
        self.fm = FlyMove(self)

        self.scene = self.loader.loadModel('models/environment')
        self.disable_mouse()

        self.scene.reparentTo(self.render)

        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)

        pandaMat = Material()
        pandaMat.setEmission((1, 0.4, 0, 1))
        colour = (0.5, 0.8, 0.8)
        expfog = Fog("Scene-wide exponential Fog object")
        expfog.setColor(*colour)
        expfog.setExpDensity(0.005)
        self.render.setFog(expfog)

        self.pandaActor = Actor('models/panda-model',
                                {'walk': 'models/panda-walk4'})
        self.pandaActor.set_material(pandaMat)
        self.pandaActor.setScale(0.005, 0.005, 0.005)
        self.pandaActor.loop('walk')
        line = NodePath('pandaline')
        for i in range(50):
            placeholder = line.attachNewNode('line-panda')
            placeholder.setPos(i * 2, 0, 0)
            self.pandaActor.instanceTo(placeholder)
        line.reparentTo(self.render)


        pandaPosIntervalInterval1 = self.pandaActor.posInterval(13,
                                                                Point3(0, -10, 0),
                                                                startPos=Point3(0, 10, 0))

        pandaPosIntervalInterval2 = self.pandaActor.posInterval(13,
                                                                Point3(0, 10, 0),
                                                                startPos=Point3(0, -10, 0))
        pandaHprIntervalInterval1 = self.pandaActor.hprInterval(2,
                                                                Point3(180, 0, 0),
                                                                startHpr=Point3(0, 0, 0))
        pandaHprIntervalInterval2 = self.pandaActor.hprInterval(2,
                                                                Point3(0, 0, 0),
                                                                startHpr=Point3(180, 0, 0))
        self.pandaPace = Sequence(pandaPosIntervalInterval1, pandaHprIntervalInterval1, pandaPosIntervalInterval2, pandaHprIntervalInterval2)

        self.pandaPace.loop()

        light = DirectionalLight('pl')
        light.set_color_temperature(2000)
        np = self.render.attachNewNode(light)
        np.set_pos(0, 0, 5)
        light.set_shadow_caster(True, 512, 512)
        self.render.setLight(np)
        # np.place()
        alight = AmbientLight('alight')
        alight.setColor(VBase4(0.3, 0.1, 0.1, 1))
        alnp = self.render.attachNewNode(alight)
        self.render.setLight(alnp)

    def spinCameraTask(self, task):
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont


app = MyApp()
app.run()
