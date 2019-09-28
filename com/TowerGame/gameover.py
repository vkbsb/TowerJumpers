__pragma__ ('skip')
document = window = Math = Date = 0 # Prevent complaints by optional static checker
PIXI = 0
__pragma__ ('noskip')

from com.pixi import PIXI
from com.TowerGame.scene import Scene
from com.TowerGame.assets import FONT_CONFIG
from com.TowerGame.gameplay import GamePlayScreen

class GameOverScreen(Scene):
    def __init__(self, rootStage):
        Scene.__init__(self, rootStage)
        self.setupScene()
        self.finished = False
    
    def replayClicked(self):
        print("Restart Clicked")
        #self.finished = True
        self.tween.reset()
        self.tween.js_from({'alpha':0}).to({'alpha':1})
        self.tween.on('end', self.markSceneDone)
        self.tween.start()

    def markSceneDone(self):
        self.finished = True

    def isComplete(self):
        return self.finished

    def setupScene(self):
        sx = 640/2
        sy = window.innerHeight/2
        
        bitmapFontText = PIXI.BitmapText('Game Over', FONT_CONFIG)
        bitmapFontText.x = sx
        bitmapFontText.y = sy - 100
        bitmapFontText.anchor.set(0.5, 0.5)
        self.stage.addChild(bitmapFontText)
        self.txt = bitmapFontText

        btnText = PIXI.BitmapText('Try Again', FONT_CONFIG)
        btnText.scale.x = 0.5
        btnText.scale.y = 0.5
        btnText.anchor.set(0.5, 0.5)
        btnText.x = sx
        btnText.y = sy + 100
        btnText.tint = 0x000000

        btn = PIXI.TilingSprite(PIXI.Texture.WHITE, btnText.width + 50, btnText.height + 15)
        btn.tint = 0x00ffee
        btn.anchor.set(0.5, 0.5)
        btn.position.x = btnText.x
        btn.position.y = btnText.y 
        btn.interactive = True
        btn.buttonMode = True
        self.stage.addChild(btn)
        self.stage.addChild(btnText)
        btn.on('click', self.replayClicked)

        overlay = PIXI.TilingSprite(PIXI.Texture.WHITE, 640, window.innerHeight)
        overlay.tint = 0x00000
        self.stage.addChild(overlay)

        tween = PIXI.tweenManager.createTween(overlay)
        tween.js_from({'alpha':1}).to({'alpha':0})
        tween.time = 500
        # self.tween.easing = PIXI.tween.Easing.inOutExpo()
        tween.start()
        self.tween = tween
