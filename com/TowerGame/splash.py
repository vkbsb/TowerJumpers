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

    def drawScene(self):
        # Set the fill color
        self.graphics.beginFill(0xe74c3c); # Red
        self.graphics.drawCircle(60, 185, 40) # drawCircle(x, y, radius)
        self.graphics.endFill()
        pass

    def update(self, dt):
        self.drawScene()
