__pragma__ ('skip')
document = window = Math = Date = 0 # Prevent complaints by optional static checker
PIXI = 0
__pragma__ ('noskip')

from com.pixi import PIXI
from com.TowerGame.camera import Camera
from com.TowerGame.scene import Scene
from com.TowerGame.gamemap import GameMap
import com.TowerGame.assets as Assets
import random

class GamePlayScreen(Scene):
    def __init__(self, rootStage):
        Scene.__init__(self, rootStage)
        self.emitter = None

        self.player = PIXI.Sprite(PIXI.Texture.WHITE)
        self.player.anchor.set(0.5, 0.5)
        self.player.height = 20
        self.player.width = 20
        self.gamePlayStage = self.stage #PIXI.Container()
        self.initGame()
        self.gamePlayStage.addChild(self.player)
        self.jumpSfx = __new__(Howl({"src":Assets.JUMP_SFX, "preload": True}))
        self.swishSfx = __new__(Howl({"src":Assets.SWISH_SFX, "preload": True}))

        window.addEventListener('keydown', self.keyDown)
        window.addEventListener('mousedown', self.mouseDown)
        window.addEventListener('touchstart', self.mouseDown)

        self.blastColors = [
            '#00ffee',
            '#f235f2',
            '#f2ff00'
        ]

        self.player.tint = random.choice(Assets.PLAYER_COLORS)

        res = PIXI.loader.resources
        texture = res[Assets.TRAIL_IMAGE].texture
        jsondata = res[Assets.TRAIL_EMITTER].data
        self.emitter = PIXI.particles.Emitter(self.gamePlayStage, [texture], jsondata)
        self.emitter.emit= True
        self.emStart = Date.now()

    def isComplete(self):
        return self.gameOver

    def playerJump(self):
        if self.player.vel[1] == 0:
            self.player.vel[1] = 15
            tween = PIXI.tweenManager.createTween(self.player)
            tween.expire = True
            final_angle = 90 if self.player.vel[0] < 0 else -90
            tween.js_from({'angle': 0}).to({'angle':final_angle})
            tween.time = 300
            tween.start()
            self.jumpSfx.play()

    def mouseDown(self, evnt):
        print("Mouse pressed") 
        self.playerJump()

    def keyDown(self, evnt):
        if evnt.key == "ArrowLeft" or evnt.code == "ArrowLeft":
            print ("Left Pressed")
        elif evnt.key == "ArrowRight" or evnt.code == "ArrowRight":
            print("Right Pressed")
            self.restartGame()
        elif evnt.key == " " or evnt.code == "Space":
            print("Jump")
            self.playerJump()


    def initGame(self):
        self.player.level = GameMap.VISIBLE_FLOORS
        self.player.vel = [4, 0]
        self.camera = Camera(self.gamePlayStage)
        self.gameOver = False
        self.score = 0

        gameArea = PIXI.Container()
        self.gameMap = GameMap(gameArea, self.player)
        self.gamePlayStage.addChild(gameArea)
        self.gameArea = gameArea

        self.player.position.x = 4 * GameMap.BLOCK_SIZE
        self.player.position.y = self.player.level * GameMap.FLOOR_HEIGHT + self.gameMap.wallThickness

    def update(self, dt):
        Scene.update(dt)
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

        self.score = Math.max(self.score, self.player.level)

        #check if this is a milestone floor. 
        if self.gameMap.isSpecial(self.player.level):
            self.gameMap.makeNormal(self.player.level)
            self.swishSfx.play()
            #add sfx on the floor. 
            levelPosY = gridY * GameMap.FLOOR_HEIGHT + GameMap.FLOOR_HEIGHT/2
            res = PIXI.loader.resources
            texture = res[Assets.SPARK_IMAGE].texture
            jsondata = res[Assets.BLAST_EMITTER].data
            for i in range(0, 5):
                jsondata.color.start = random.choice(self.blastColors)
                emitter = PIXI.particles.Emitter(self.gamePlayStage, [texture], jsondata)
                emitter.ownerPos.y = levelPosY
                emitter.ownerPos.x = random.choice(range(GameMap.BLOCK_SIZE, 20*GameMap.BLOCK_SIZE))
                emitter.emit= True
                emitter.playOnceAndDestroy()
                emitter.autoUpdate = True

        self.gameMap.applyFloorEffect(self.player.level, self.player.tint)
            
        if self.emitter:
            self.emitter.ownerPos.x = self.player.position.x
            self.emitter.ownerPos.y = self.player.position.y
            ts = Date.now()
            self.emitter.js_update((ts-self.emStart) * 0.001)
            self.emStart = ts
    
    def cleanup(self):
        Scene.cleanup(self)
        window.removeEventListener('keydown', self.keyDown)
        window.removeEventListener('mouseDown', self.mouseDown)
        window.removeEventListener('touchstart', self.mouseDown)
