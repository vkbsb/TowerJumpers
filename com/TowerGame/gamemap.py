__pragma__ ('skip')
document = window = Math = Date = 0 # Prevent complaints by optional static checker
PIXI = 0
__pragma__ ('noskip')

import random
from com.pixi import PIXI

class GameMap:
    BLOCK_SIZE = 15
    FLOOR_HEIGHT = 100
    FLOOR = '_'
    WALL = '|'
    GAP = ' '
    VISIBLE_FLOORS = 4
    FLOOR_SETS = [
        [
            '          _____________|',
            '______________',
            '|_____________',
            '          _____________|',
        ],
        [
            '|_____________          |',
            '|          _____________|',
            '|_____________|',
            '|_____________|',
        ],
        [
            '|____________       _____',
            '|          __________',
            '|_____________',
            '|___________      ',
            '|________________|',
        ]
    ]
    def __init__(self, gameArea):
        floors = [
            '|_____________________|',
            '|_____________________|',
            '      _____________________',
            '|_________________________________|',
            '|__    _______________|',
            '      _____________________',
            '|_____________________|',
            '|__________      _________________',
            '|_________________________________|',
            '|______________________',
            '|_____________        ________',
            '|_____________________|',
        ]        
        floors.reverse()
        self.floors = floors
        blockSize = GameMap.BLOCK_SIZE
        floorHeight = GameMap.FLOOR_HEIGHT
        xOffset = 0
        yOffset = 0
        self.gameArea = gameArea
        #[0] tracks the current level for the head and tail. [1] track the modulo floors. 
        self.floorTail = [0, 0]
        self.floorHead = [len(self.floors)-1, len(self.floors)-1]
        self.floorSprites = []
        
        #usage for input callback.
        self.xOffset = xOffset
        self.yOffset = yOffset
        self.wallThickness = 5

        #floor set
        self.floorSet = 0
        self.floorSetOffset = 0

        for level, floorplan in enumerate(floors):
            floor = self.createFloorSprite(floorplan)
            floor.position.y = yOffset + level * GameMap.FLOOR_HEIGHT
            gameArea.addChild(floor)
            self.floorSprites.append(floor)

    def createFloorSprite(self, floorplan):
        floor = PIXI.Container()
        prevX = 0
        xOffset = 0
        prevChar = GameMap.GAP
        if floorplan[0] == GameMap.WALL:
            prevChar = GameMap.FLOOR
        
        floorLength = len(floorplan)
        walls = []
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
            if block == GameMap.WALL:
                walls.append(x)

        for wall in walls:
            spr = PIXI.TilingSprite(PIXI.Texture.WHITE, self.wallThickness, GameMap.FLOOR_HEIGHT)
            spr.position.x = xOffset + wall * GameMap.BLOCK_SIZE
            floor.addChild(spr)

        # #left cap
        # if floorplan[0] == GameMap.WALL:
        #     spr = PIXI.TilingSprite(PIXI.Texture.WHITE, self.wallThickness, GameMap.FLOOR_HEIGHT)
        #     spr.position.x = xOffset
        #     floor.addChild(spr)
        # #right cap
        # if floorplan[floorLength-1] == GameMap.WALL:
        #     spr = PIXI.TilingSprite(PIXI.Texture.WHITE, self.wallThickness, GameMap.FLOOR_HEIGHT)
        #     spr.position.x = xOffset + (floorLength-1) * GameMap.BLOCK_SIZE
        #     floor.addChild(spr)
        return floor

    def getFloorPlan(self, level):        
        if level > self.floorTail[0]:
            off_level = level % len(self.floors)
            return self.floors[off_level]

    def update(self, player):
        # print("floorTail: ", Math.max(0, player.level - GameMap.VISIBLE_FLOORS))
        floorTail = Math.max(0, player.level - GameMap.VISIBLE_FLOORS)
        if floorTail > self.floorTail[0]:
            #wrap around the end tag and move the floor sprite.
            delta = 1 #we are sure to get delta 1 everytime.             
            self.floorHead[0] += delta
            self.floorHead[1] = (self.floorHead[1] + delta ) % len(self.floors)

            #update the floorplan that is pointed to by the floorHead[1] in floors 
            #create new sprite for the floor and then set the position.
            floorSet =  GameMap.FLOOR_SETS[self.floorSet]           
            floorplan = floorSet[self.floorSetOffset]
            floorIndex = self.floorHead[1]
            self.floorSprites[floorIndex]
            self.gameArea.removeChild(self.floorSprites[floorIndex])
            self.floors[floorIndex] = floorplan
            #optimize by pre-creating?
            floorSprite = self.createFloorSprite(floorplan)
            self.gameArea.addChild(floorSprite)            
            floorSprite.position.y = self.yOffset + GameMap.FLOOR_HEIGHT * self.floorHead[0]
            #update the floorsetoffset to point to the next floorplan to pick.
            self.floorSetOffset += 1
            if self.floorSetOffset >= len(floorSet):
                self.floorSet = random.choice(range(0, len(GameMap.FLOOR_SETS)))
                self.floorSetOffset = 0

            self.floorSprites[floorIndex] = floorSprite
            self.floorTail[0] += delta
            self.floorTail[1] = (self.floorTail[1] + delta) % len(self.floors)