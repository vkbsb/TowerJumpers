__pragma__ ('noanno')
__pragma__('js', '{}', __include__('com/howler/__javascript__/howler.js'))


def PyHowl(*args):
    return __new__(Howl(*args))