__pragma__ ('skip')
document = window = Math = Date = 0 # Prevent complaints by optional static checker
PIXI = 0
__pragma__ ('noskip')

import random
from com.pixi import PIXI
from com.TowerGame.gamemap import GameMap
from com.TowerGame.camera import Camera

class Game:
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

        self.app = app
        document.body.appendChild(app.view)

        self.player = PIXI.Sprite(PIXI.Texture.WHITE)
        self.player.tint = 0xff0000
        self.player.level = 4
        self.player.vel = [2, 0]
        self.player.anchor.set(0.5, 0)
        self.player.height = 32
        self.app.stage.addChild(self.player)
        self.camera = Camera(app)

        window.addEventListener('keydown', self.keyDown)
        #game setup
        self.setup()

        #schedule update for the game loop.    
        PIXI.Ticker.shared.add(self.update)

    def keyDown(self, evnt):
        if evnt.key == "ArrowLeft" or evnt.code == "ArrowLeft":
            print ("Left Pressed")
        elif evnt.key == "ArrowRight" or evnt.code == "ArrowRight":
            print("Right Pressed")
        elif evnt.key == " " or evnt.code == "Space":
            print("Jump")
            # self.player.level += 1
            # self.player.position.y = self.yOffset + self.player.level * self.floorHeight + self.wallThickness
            self.player.vel[1] = 15
                      

    def setup(self):
        #game related stuff
        gameArea = PIXI.Container()
        self.gameMap = GameMap(gameArea)
        self.app.stage.addChild(gameArea)
        self.gameArea = gameArea

        self.player.position.x = 2 * GameMap.BLOCK_SIZE
        self.player.position.y = self.player.level * GameMap.FLOOR_HEIGHT + self.gameMap.wallThickness

    def update(self, dt):
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
 
        PIXI.tweenManager.js_update()