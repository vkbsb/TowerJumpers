__pragma__ ('skip')
document = window = Math = Date = 0 # Prevent complaints by optional static checker
PIXI = 0
__pragma__ ('noskip')

import random
from com.pixi import PIXI
import com.howler
from com.TowerGame.assets import PLAYER_COLORS

class GameMap:
    BLOCK_SIZE = 15
    FLOOR_HEIGHT = 100
    FLOOR = '_'
    WALL = '|'
    GAP = ' '
    VISIBLE_FLOORS = 4
    FLOOR_SETS = [
        [
            '|_____________|',
            '|_____________|',
            '          _____________|',
            '______________',
            '|_____________',
            '          _____________|',
            '|_____________',
            '          _____________|',
            '|_____________|',
            '|_____________|',
        ],
        [
            '       |_________|',
            '|_________',
            '        _________|',
            '|_________',
            '|       _________|',
            '|___________',
            '|___________      ',
            '          _______|',
            '          _______|',
            '|________________|',
        ],
        [
            '|________________|',
            '     _____',
            '|_________________________________|',
            '   |________________|',
            '|________     ________|',
            '            __________|',
            '  |__________',
            '         |________________|',
            '|_________________________________|',
            '|_________________________________|',
        ],
         [            
            '|_____________________|',
            '      |_____________________|',
            '|__    _______________|',
            '|_____________________|',
            '|_____________________|',
            '|__________      _________________|',
            '|_________________________________|',
            '      |______________________',
            '      |_____________        ________',
            '      |_____________________|',
        ],       
        [
            '|________________|',
            '    _____',
            '|________________|',
            '            _____',
            '|________________|',
            '    _____',
            '|_____________|',
            '         |________________|',
            '|_______________',
            '|________|',
        ],
        [
            '|________________|',
            '    |____________',
            '     ____________',
            '     ____________',
            '              __________|',
            '              __________',
            '              __________',
            '      |__________',
            '      ___________',
            '|______________|',
        ],
       [
            '|________________|',
            '         ________',
            '             _______',
            '                    _______',
            '                       ________|',
            '                    _______',
            '             _______',
            '         ________',
            '    ________',
            '|______________|',
        ],
        [
            '|________________|',
            '    _____',
            '      |__________|',
            '            _____',
            '              |__________|',
            '                       _____',
            '                 ______________|',
            '              _____',
            '           _____',
            '|_______________|',
        ],
        [
            '|________________|',
            '      _____',
            '  |_____',
            '       _____|',
            '    _____',
            '|_____',
            '    _____',
            '       _____|',
            '    _____',
            '|______________|',
        ],
        [
            '|_________________|',
            '    |_____________',
            '                  _____',
            '                     __________|',
            '                     _____',
            '            |__________',
            '                  _____',
            '                     __________|',
            '                     _____',
            '|________________________|',
        ],
        [
            '|_________________________________|',
            '               _____|',
            '           |_____',
            '               _____|',
            '           |_____',
            '               _____|',
            '           |_____',
            '               _____|',
            '           |_____',
            '|_________________________________|',
        ],
        [
            '|_________________________________|',
            '___________________________________',
            '_______________      ______________',
            '|_____                      _____|',
            '    _____                _____',
            '       _____          _____',
            '           |__________|',
            '            __________',
            '               _____',
            '|_________________________________|',
        ],
    ]
    def __init__(self, gameArea):
        floors = [            
            '|_____________________|',
            '      |_____________________|',
            '|__    _______________|',
            '|_____________________|',
            '|_____________________|',
            '|__________      _________________|',
            '|_________________________________|',
            '      |______________________',
            '      |_____________        ________',
            '      |_____________________|',
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

        self.fullRandom = False
        if window.localStorage['highscore']:
            val = int(window.localStorage['highscore'])
            if val > 50:
                self.fullRandom = True
        
        for level, floorplan in enumerate(floors):
            floor = self.createFloorSprite(floorplan)
            floor.position.y = yOffset + level * GameMap.FLOOR_HEIGHT
            gameArea.addChild(floor)
            self.floorSprites.append(floor)

    def createFloorSprite(self, floorplan, showFloorNumber=False):
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
            elif block == GameMap.FLOOR and (prevChar == GameMap.GAP or prevChar == GameMap.WALL): #found the next floor. 
                prevX = x
                #solve the bug where the left wal was one block gap away from the rest of the floor. 
                if prevChar == GameMap.WALL:
                    prevX -= 1
                prevChar = GameMap.FLOOR
            if block == GameMap.WALL:
                walls.append(x)
                prevChar = GameMap.WALL

        for wall in walls:
            spr = PIXI.TilingSprite(PIXI.Texture.WHITE, self.wallThickness, GameMap.FLOOR_HEIGHT)
            spr.position.x = xOffset + wall * GameMap.BLOCK_SIZE
            floor.addChild(spr)

        if len(walls) > 0 and showFloorNumber == True:
            #if the floor is special add the floor number to left corner of the level. 
            bitmapFontText = PIXI.BitmapText('{}'.format(self.floorHead[0]), { 'font': '64px Roboto', 'align': 'center' })
            bitmapFontText.x = xOffset + walls[0] * GameMap.BLOCK_SIZE + self.wallThickness
            bitmapFontText.y = GameMap.FLOOR_HEIGHT
            bitmapFontText.scale.y = -0.5
            bitmapFontText.scale.x = 0.5
            bitmapFontText.js_name = "txt"
            # bitmapFontText.anchor.set(0.5, 0.5)

            #add the bar background
            colors = []
            bh = (GameMap.FLOOR_HEIGHT-self.wallThickness) / float(len(PLAYER_COLORS))
            for indx, clr in enumerate(PLAYER_COLORS):
                bg = PIXI.TilingSprite(PIXI.Texture.WHITE, (walls[1]-walls[0]) * GameMap.BLOCK_SIZE-self.wallThickness, bh)
                bg.tint = clr
                bg.position.y = indx * bh + self.wallThickness
                bg.position.x = xOffset + walls[0] * GameMap.BLOCK_SIZE + self.wallThickness
                bg.js_name = "bg"+str(indx)
                bg.visible = False
                floor.addChild(bg)
            floor.addChild(bitmapFontText)
            
        return floor

    def getFloorPlan(self, level):        
        if level > self.floorTail[0]:
            off_level = level % len(self.floors)
            return self.floors[off_level]

    def isSpecial(self, level):
        off_level = level % len(self.floors)
        return self.floorSprites[off_level].name == "fx"
    
    def makeNormal(self, level):
        off_level = level % len(self.floors)
        floorSprite = self.floorSprites[off_level]
        if floorSprite.name.startsWith("fx"):
            for indx in range(0, len(PLAYER_COLORS)):
                spr = floorSprite.getChildByName("bg" + str(indx))
                spr.visible = True 
                tween = PIXI.tweenManager.createTween(spr)
                tween.expire = True
                # spr.alpha = 0.5
                tween.delay = 200
                if indx == 1:                
                    tween.js_from({'width': 0, 'x':spr.position.x+spr.width}).to({'width':spr.width, 'x':spr.position.x})
                else:
                    tween.js_from({'width': 0}).to({'width':spr.width})
                tween.time = 250
                tween.start()
                spr.width = 0
                
        floorSprite.name = "normal"
    
    def applyFloorEffect(self, level, color):
        off_level = level % len(self.floors)
        floorSprite = self.floorSprites[off_level]
        if floorSprite.accessibleTitle:
            return False
        for spr in floorSprite.children:
            if spr.height <= self.wallThickness:
                spr.tint = color
        floorSprite.accessibleTitle = "cx"

        txt = floorSprite.getChildByName("txt")
        if txt:
            txt.tint = 0x000000
        return True

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
            if self.floorHead[0] in (20, 40) or self.floorHead[0] % 50 == 0:                
                floorSprite = self.createFloorSprite(floorplan, True)
                floorSprite.name = "fx"
            else:
                floorSprite = self.createFloorSprite(floorplan)
            self.gameArea.addChild(floorSprite)
            floorSprite.position.y = self.yOffset + GameMap.FLOOR_HEIGHT * self.floorHead[0]
            #update the floorsetoffset to point to the next floorplan to pick.
            self.floorSetOffset += 1
            if self.floorSetOffset >= len(floorSet):
                if self.floorHead[0] > 60 or self.fullRandom == True:
                    self.floorSet = random.choice(range(0, len(GameMap.FLOOR_SETS)))
                else:
                    self.floorSet += 1                    
                self.floorSetOffset = 0

            self.floorSprites[floorIndex] = floorSprite
            self.floorTail[0] += delta
            self.floorTail[1] = (self.floorTail[1] + delta) % len(self.floors)