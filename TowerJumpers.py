__pragma__ ('skip')
document = window = Math = Date = 0 # Prevent complaints by optional static checker
PIXI = 0
__pragma__ ('noskip')

import random
from com.pixi import PIXI

class Game:
    FLOOR = '_'
    WALL = '|'
    GAP = ' '
    def __init__(self):
        app = PIXI.Application({"width":256, "height":256, 'antialias': True})

        #set full screen rendering
        app.renderer.view.style.position = "absolute"
        app.renderer.view.style.display = "block"
        app.renderer.autoDensity = True
        app.renderer.resize(window.innerWidth, window.innerHeight)
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
        self.app.stage.position.y = app.renderer.height / app.renderer.resolution
        self.app.stage.scale.y = -1
        self.cameraTween = PIXI.tweenManager.createTween(self.app.stage)

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
        floors = [
            '|_____________________|',
            '|_____________________|',
            '      _____________________',
            '|_________________________________|',
            '|__    _______________|',
            '      _____________________',
            '|_____________________|',
            '      _________________',
            '|_________________________________|',
            '|______________________',
            '|_____________        ________',
            '|_____________________|',
        ]
        self.floors = floors
        gameArea = PIXI.Container() #self.app.stage

        w = window.innerWidth * 0.3
        h = window.innerHeight

        blockSize = 15
        floorHeight = h / 10
        xOffset = 0 #window.innerWidth * 0.5 - w/2.0
        yOffset = 0

        #usage for input callback.
        self.blockSize = blockSize
        self.floorHeight = floorHeight
        self.xOffset = xOffset
        self.yOffset = yOffset
        self.wallThickness = 5

        self.player.position.x = xOffset + 2 * blockSize
        self.player.position.y = yOffset + self.player.level * floorHeight + self.wallThickness

        for level, floorplan in enumerate(floors):
            prevX = 0
            prevChar = Game.GAP
            if floorplan[0] == Game.WALL:
                prevChar = Game.FLOOR
            
            floorLength = len(floorplan)
            for x, block in enumerate(floorplan):
                if (block == Game.GAP or x == floorLength - 1) and prevChar == Game.FLOOR: #found first gap
                    l = x - prevX
                    spr = PIXI.TilingSprite(PIXI.Texture.WHITE, l * blockSize, self.wallThickness)
                    spr.position.x = xOffset + prevX * blockSize
                    spr.position.y = yOffset + level * floorHeight
                    gameArea.addChild(spr)
                    prevChar = Game.GAP
                elif block == Game.FLOOR and prevChar == Game.GAP: #found the next floor. 
                    prevX = x
                    prevChar = Game.FLOOR
            #left cap
            if floorplan[0] == Game.WALL:
                spr = PIXI.TilingSprite(PIXI.Texture.WHITE, self.wallThickness, floorHeight)
                spr.position.x = xOffset
                spr.position.y = yOffset + level * floorHeight
                gameArea.addChild(spr)
            #right cap
            if floorplan[floorLength-1] == Game.WALL:
                spr = PIXI.TilingSprite(PIXI.Texture.WHITE, self.wallThickness, floorHeight)
                spr.position.x = xOffset + (floorLength-1) * blockSize
                spr.position.y = yOffset + level * floorHeight
                gameArea.addChild(spr)
        self.app.stage.addChild(gameArea)
        self.gameArea = gameArea

    def moveCamera(self):
        cameraPlayerOffset = 600
        self.cameraTween.reset()
        self.cameraTween.js_from({'y':self.app.stage.position.y}).to({'y':self.player.position.y + cameraPlayerOffset})
        self.cameraTween.time = 800
        # self.cameraTween.easing = PIXI.tween.Easing.inOutExpo()
        self.cameraTween.start()

    def update(self, dt):
        if(self.player.vel[1] > 0):
            self.player.vel[1] -= dt * 1
        elif self.player.vel[1] < 0:
            self.player.vel[1] -= dt * 2
        newY = self.player.position.y + dt * self.player.vel[1]
        newX = self.player.position.x + dt * self.player.vel[0]

        #find the grid position of the newX
        gridX = Math.round((newX-self.xOffset) / self.blockSize)
        gridY = Math.round((newY-self.yOffset) / self.floorHeight)

        if gridX < 0 or gridX > len(self.floors[gridY]):
            self.player.vel[1] -= 0.1            
            gridY = gridY-1        

        c = self.floors[gridY][gridX]
        if c == Game.WALL:
            self.player.vel[0] *= -1        

        if self.player.vel[1] == 0:
            if c == Game.GAP:
                self.player.vel[1] = -1                
        elif self.player.vel[1] < 0:
            levelPosY = self.yOffset + gridY * self.floorHeight + self.wallThickness            
            if newY <  levelPosY and self.floors[gridY][gridX] == Game.FLOOR:
                newY = levelPosY
                self.player.vel[1] = 0
                self.player.level = gridY                

        self.moveCamera()
        self.player.position.x = newX
        self.player.position.y = newY
 

        PIXI.tweenManager.js_update()

Game()


