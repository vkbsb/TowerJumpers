__pragma__ ('skip')
document = window = Math = Date = 0 # Prevent complaints by optional static checker
PIXI = 0
__pragma__ ('noskip')

from com.pixi import PIXI
from com.TowerGame.gamemap import GameMap

class Camera:
    def __init__(self, gameplayLayer):        
        self.stage = gameplayLayer        
        self.stage.position.y = window.innerHeight
        self.stage.scale.y = -1
        self.tween = PIXI.tweenManager.createTween(self.stage)
        self.cameraPlayerOffset = window.innerHeight/2.0#GameMap.FLOOR_HEIGHT * 5 #assuming we want the player to be 4th floor on start.

    def centerOn(self, player):
        self.tween.reset()
        self.tween.js_from({'y':self.stage.position.y}).to({'y':player.position.y + self.cameraPlayerOffset})
        self.tween.time = 800
        # self.tween.easing = PIXI.tween.Easing.inOutExpo()
        self.tween.start()
