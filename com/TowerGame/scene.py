__pragma__ ('skip')
document = window = Math = Date = 0 # Prevent complaints by optional static checker
PIXI = 0
__pragma__ ('noskip')

from com.pixi import PIXI

class Scene:
    def __init__(self, rootStage):
        self.stage = PIXI.Container()
        rootStage.addChild(self.stage)

    def setVisible(self, value):
        self.stage.visible = value

    def update(self, dt):
        pass

    def cleanup(self):
        print("Deleting Scene")
        self.stage.parent.removeChild(self.stage)