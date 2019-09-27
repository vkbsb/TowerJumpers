__pragma__ ('noanno')

__pragma__('js', '{}', __include__('com/pixi/__javascript__/pixi.min.js'))
__pragma__('js', '{}', __include__('com/pixi/__javascript__/pixi-dragonbones.js'))
__pragma__('js', '{}', __include__('com/pixi/__javascript__/pixi-particles.js'))
__pragma__('js', '{}', __include__('com/pixi/__javascript__/pixi-tween.js'))

def _ctor(obj):
    def _c_(*args):
        return __new__(obj (*args))
    return _c_

#PIXI variable is defined by the JS included above. 
api = PIXI
dragonBones = window.dragonBones

#get rid of the global instances of PIXI and dragonBones.
__pragma__('js', '{}', 'delete window.dragonBones; delete window.PIXI;')

#PIXI object to be exposed for python to use. We are doing this to avoid writing __new__ in the python app code.
PIXI = {}
PIXI.Application = _ctor(api.Application)
PIXI.Container = _ctor(api.Container)
PIXI.loader = api.loader
PIXI.utils = api.utils
PIXI.TilingSprite = _ctor(api.TilingSprite)
PIXI.Sprite = _ctor(api.Sprite)
PIXI.Texture = api.Texture
PIXI.Ticker = api.Ticker
PIXI.settings = api.settings
PIXI.Rectangle = _ctor(api.Rectangle)
PIXI.VERSION = api.VERSION
PIXI.DRAW_MODES = api.DRAW_MODES
PIXI.SimpleMesh = _ctor(api.SimpleMesh)
PIXI.Graphics = _ctor(api.Graphics)
PIXI.particles = api.particles
PIXI.particles.Emitter = _ctor(api.particles.Emitter)
PIXI.ParticleContainer = _ctor(api.ParticleContainer)
PIXI.BitmapText = _ctor(api.BitmapText)

PIXI.tweenManager = api.tweenManager
PIXI.tween = api.tween
