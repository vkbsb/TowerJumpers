__pragma__ ('skip')
document = window = Math = Date = 0 # Prevent complaints by optional static checker
PIXI = 0
__pragma__ ('noskip')

from com.pixi import PIXI
from com.TowerGame.scene import Scene



class LoadingScreen(Scene):
    def __init__(self, rootStage):        
        Scene.__init__(self, rootStage)
        self.graphics = PIXI.Graphics()
        # self.drawScene()
        self.stage.addChild(self.graphics)
        self.time = 0

    def drawScene(self, dt):
        self.graphics.js_clear()
        # Set the fill color
        self.graphics.beginFill(0xe74c3c); # Red
        sx = 640/2.0
        sy = window.innerHeight / 2.0
        r = 20
        offset = 50

        self.graphics.drawCircle(sx - offset, sy, r * Math.abs(Math.sin(self.time*0.05))) # drawCircle(x, y, radius)
        self.graphics.drawCircle(sx, sy, r * Math.abs(Math.sin(self.time*0.05 + Math.PI/6))) # drawCircle(x, y, radius)
        self.graphics.drawCircle(sx + offset, sy, r * Math.abs(Math.sin(self.time*0.05 + Math.PI/3))) # drawCircle(x, y, radius)
        self.graphics.endFill()
        self.time += dt
        pass

    def update(self, dt):
        self.drawScene(dt)
