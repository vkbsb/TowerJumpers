__pragma__ ('skip')
document = window = Math = Date = 0 # Prevent complaints by optional static checker
PIXI = 0
__pragma__ ('noskip')

import random
from com.pixi import PIXI

class GameMap:
    BLOCK_SIZE = 10
    FLOOR_HEIGHT = 100
    FLOOR = '_'
    WALL = '|'
    GAP = ' '
    def __init__(self, gameArea):
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
        blockSize = GameMap.BLOCK_SIZE
        floorHeight = GameMap.FLOOR_HEIGHT
        xOffset = 0
        yOffset = 0
        self.gameArea = gameArea
        
        #usage for input callback.
        self.xOffset = xOffset
        self.yOffset = yOffset
        self.wallThickness = 5

        for level, floorplan in enumerate(floors):
            floor = self.createFloorSprite(floorplan)
            floor.position.y = yOffset + level * GameMap.FLOOR_HEIGHT
            gameArea.addChild(floor)

    def createFloorSprite(self, floorplan):
        floor = PIXI.Container()
        prevX = 0
        xOffset = 0
        prevChar = GameMap.GAP
        if floorplan[0] == GameMap.WALL:
            prevChar = GameMap.FLOOR
        
        floorLength = len(floorplan)
        for x, block in enumerate(floorplan):
            if (block == GameMap.GAP or x == floorLength - 1) and prevChar == GameMap.FLOOR: #found first gap
                l = x - prevX
                spr = PIXI.TilingSprite(PIXI.Texture.WHITE, l * GameMap.BLOCK_SIZE, self.wallThickness)
                spr.position.x = xOffset + prevX * GameMap.BLOCK_SIZE
                floor.addChild(spr)
                prevChar = GameMap.GAP
            elif block == GameMap.FLOOR and prevChar == GameMap.GAP: #found the next floor. 
                prevX = x
                prevChar = GameMap.FLOOR
        #left cap
        if floorplan[0] == GameMap.WALL:
            spr = PIXI.TilingSprite(PIXI.Texture.WHITE, self.wallThickness, GameMap.FLOOR_HEIGHT)
            spr.position.x = xOffset
            floor.addChild(spr)
        #right cap
        if floorplan[floorLength-1] == GameMap.WALL:
            spr = PIXI.TilingSprite(PIXI.Texture.WHITE, self.wallThickness, GameMap.FLOOR_HEIGHT)
            spr.position.x = xOffset + (floorLength-1) * GameMap.BLOCK_SIZE
            floor.addChild(spr)
        return floor

    def getFloorPlan(self, level):
        if level >= 0 and level < len(self.floors):
            return self.floors[level]
