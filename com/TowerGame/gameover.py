__pragma__ ('skip')
document = window = Math = Date = 0 # Prevent complaints by optional static checker
PIXI = 0
__pragma__ ('noskip')

from com.pixi import PIXI
from com.TowerGame.scene import Scene

class GameOverScreen(Scene):
    def __init__(self, rootStage):
        Scene.__init__(self, rootStage)
        self.setupScene()

    def setupScene(self):
        bitmapFontText = PIXI.BitmapText('Hello World', { 'font': '64px Roboto', 'align': 'center' })
        bitmapFontText.x = 640/2
        bitmapFontText.y = bitmapFontText.height
        bitmapFontText.anchor.set(0.5, 0.5)
        self.stage.addChild(bitmapFontText)
        self.txt = bitmapFontText