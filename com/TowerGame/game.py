__pragma__ ('skip')
document = window = Math = Date = 0 # Prevent complaints by optional static checker
PIXI = 0
__pragma__ ('noskip')

from com.pixi import PIXI
from com.TowerGame.gamemap import GameMap
from com.TowerGame.camera import Camera

class Game:
    TRAIL_IMAGE = "assets/images/Pixel25px.png"
    TRAIL_EMITTER = "assets/trail_effect.json"
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

        #reverse the GameMap stuff  
        for floorSet in GameMap.FLOOR_SETS:
            floorSet.reverse()

        PIXI.loader.add([Game.TRAIL_EMITTER, Game.TRAIL_IMAGE])
        PIXI.loader.load(self.onAssetsLoaded)
        self.emitter = None

        self.player = PIXI.Sprite(PIXI.Texture.WHITE)
        self.player.tint = 0xff0000
        self.player.level = GameMap.VISIBLE_FLOORS
        self.player.vel = [4, 0]
        self.player.anchor.set(0.5, 0)
        self.player.height = 32
        self.app.stage.addChild(self.player)
        self.camera = Camera(app)

        window.addEventListener('keydown', self.keyDown)
        #game setup
        self.setup()

        #schedule update for the game loop.    
        PIXI.Ticker.shared.add(self.update)

    def onAssetsLoaded(self):
        res = PIXI.loader.resources
        texture = res[Game.TRAIL_IMAGE].texture
        jsondata = res[Game.TRAIL_EMITTER].data
        self.emitter = PIXI.particles.Emitter(self.app.stage, [texture], jsondata)
        self.emitter.emit= True
        self.emStart = Date.now()
        #self.player.addChild()
        pass

    def keyDown(self, evnt):
        if evnt.key == "ArrowLeft" or evnt.code == "ArrowLeft":
            print ("Left Pressed")
        elif evnt.key == "ArrowRight" or evnt.code == "ArrowRight":
            print("Right Pressed")
            self.restartGame()
        elif evnt.key == " " or evnt.code == "Space":
            print("Jump")
            if self.player.vel[1] == 0:
                self.player.vel[1] = 15
                      
    def restartGame(self):
        self.player.vel = [4, 0]
        self.player.level = GameMap.VISIBLE_FLOORS
        self.camera = Camera(self.app)
        self.app.stage.removeChild(self.gameArea)
        self.setup()
        self.gameOver = False

    def setup(self):
        #game related stuff
        gameArea = PIXI.Container()
        self.gameMap = GameMap(gameArea, self.player)
        self.app.stage.addChild(gameArea)
        self.gameArea = gameArea

        self.player.position.x = 2 * GameMap.BLOCK_SIZE
        self.player.position.y = self.player.level * GameMap.FLOOR_HEIGHT + self.gameMap.wallThickness

    def update(self, dt):
        if self.gameOver:
            return

        if(self.player.vel[1] > 0):
            self.player.vel[1] -= dt * 1
        elif self.player.vel[1] < 0:
            self.player.vel[1] -= dt * 2
        newY = self.player.position.y + dt * self.player.vel[1]
        newX = self.player.position.x + dt * self.player.vel[0]

        #find the grid position of the newX
        gridX = Math.round((newX) / GameMap.BLOCK_SIZE)
        gridY = Math.round((newY) / GameMap.FLOOR_HEIGHT)

        floorPlan = self.gameMap.getFloorPlan(gridY)

        if gridX < 0 or gridX > len(floorPlan):
            self.player.vel[1] -= 0.1            
            gridY = gridY-1
            floorPlan = self.gameMap.getFloorPlan(gridY)
            #TODO: handle the case where gridX is negative. We have to end the game.  

        if not floorPlan or self.player.level < self.gameMap.floorTail:
            self.gameOver = True
            print("Game Over")
            self.restartGame()
            return
            
        c = floorPlan[gridX]
        if c == GameMap.WALL:
            self.player.vel[0] *= -1        

        if self.player.vel[1] == 0:
            if c == GameMap.GAP:
                self.player.vel[1] = -1                
        elif self.player.vel[1] < 0:
            levelPosY = gridY * GameMap.FLOOR_HEIGHT + self.gameMap.wallThickness
            if newY <  levelPosY and floorPlan[gridX] == GameMap.FLOOR:
                newY = levelPosY
                self.player.vel[1] = 0
                self.player.level = gridY

        self.camera.centerOn(self.player)
        self.player.position.x = newX
        self.player.position.y = newY
        self.gameMap.update(self.player)

        if self.emitter:
            self.emitter.ownerPos.x = self.player.position.x
            self.emitter.ownerPos.y = self.player.position.y
            ts = Date.now()
            self.emitter.js_update((ts-self.emStart) * 0.001)
            self.emStart = ts
 
        PIXI.tweenManager.js_update()