__pragma__ ('skip')
document = window = Math = Date = 0 # Prevent complaints by optional static checker
PIXI = 0
__pragma__ ('noskip')

from com.pixi import PIXI
from com.TowerGame.gamemap import GameMap
from com.TowerGame.camera import Camera
from com.TowerGame.gameplay import GamePlayScreen
from com.TowerGame.splash import LoadingScreen
from com.TowerGame.gameover import GameOverScreen
import com.TowerGame.assets as Assets

class Game:
    LOADING_SCREEN = 0
    TITLE_SCREEN = 1
    GAMEPLAY_SCREEN = 2
    GAMEOVER_SCREEN = 3

    def __init__(self):
        app = PIXI.Application({"width":640, "height":960, 'antialias': True})

        #set full screen rendering
        app.renderer.view.style.position = "absolute"
        app.renderer.view.style.display = "block"
        app.renderer.view.style.marginLeft = "-320px"
        app.renderer.view.style.left = "50%"
        app.renderer.autoDensity = True
        #fix the width and change height based on device.
        app.renderer.resize(640, window.innerHeight)
        # app.renderer.resize(window.innerWidth, window.innerHeight)
        # app.renderer.backgroundColor = 0xffffff
        self.gameOver = False
        self.app = app
        document.body.appendChild(app.view)
        self.state = Game.LOADING_SCREEN
        self.screen = LoadingScreen(self.app.stage) #LoadingScreen(self.app.stage)


        #reverse the GameMap stuff  
        for floorSet in GameMap.FLOOR_SETS:
            for indx, floorplan in enumerate(floorSet):
                floorSet[indx] = "    " + floorplan
            floorSet.reverse()

        PIXI.loader.add([Assets.TRAIL_EMITTER, 
            Assets.TRAIL_IMAGE, 
            Assets.BITMAP_FONT,
            Assets.SPARK_IMAGE,
            Assets.BLAST_EMITTER])

        PIXI.loader.load(self.onAssetsLoaded)

        #game setup
        self.setup()

        #schedule update for the game loop.    
        PIXI.Ticker.shared.add(self.update)

    def onAssetsLoaded(self):
        #self.player.addChild()
        self.screen.cleanup()
        print("StageChildren: ", self.app.stage.children.length)
        self.screen = GamePlayScreen(self.app.stage)
        self.state = Game.GAMEPLAY_SCREEN

    def setup(self):
        #game related stuff
        pass

    def update(self, dt):
        self.screen.update(dt)
        if self.state == Game.GAMEPLAY_SCREEN:
            if self.screen.gameOver:
                self.screen.cleanup()
                self.screen = GameOverScreen(self.app.stage)
                self.state = Game.GAMEOVER_SCREEN
        if self.state == Game.GAMEOVER_SCREEN:
            pass
        PIXI.tweenManager.js_update()