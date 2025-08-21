import json
import time

# Config


KNOWN_ANIMATIONS = ["cry", "grin_sweet", "happy", "joy", "laugh", "scream", "tongue", "wink"]
DEFAULT_ANIMATION = "happy"

USE_COLOR = True


class Animation:

    def __init__(self, name: str, file: str):
        self.__name = name

        with open(file) as fp:
            frames = json.load(fp)

            self.__frames = []

            lastClr = (-1,-1,-1)

            # Constructs the frames
            for frame in frames:
                    constr = ""
                    for line in frame:
                        for pxl in line:

                            # Adds the pixel and color code before
                            if USE_COLOR:
                                r = pxl['r']
                                g = pxl['g']
                                b = pxl['b']

                                if lastClr != (r,g,b):
                                    constr += f'\x1b[38;2;{r};{g};{b}m'
                                    lastClr = (r,g,b)

                            constr += pxl['c']
                        constr += '\n'
                    self.__frames.append(constr)
    
    def getName(self):
        return self.__name

    def getLength(self):
        return len(self.__frames)

    def showFrame(self, frame: int, clear_screen: bool = True):
        data = ""

        if clear_screen:
            data += '\x1bc'

        data += self.__frames[frame]

        print(data)


# Currently playing animation
currentAnimation: Animation = None
currentFrame: int = 0
nextFrameTime = -1

def loadAnimation(anim: str):
    global currentAnimation, currentFrame

    # Load animation
    currentFrame = 0
    currentAnimation = Animation(anim, f'client/animations/{anim}.json')

def onSelectAnimation(anim: str = DEFAULT_ANIMATION):
    global currentAnimation, DEFAULT_ANIMATION, KNOWN_ANIMATIONS, currentFrame, currentAnimation

    # Prevent if there is an animation playing
    if currentAnimation != None and currentAnimation.getName() != DEFAULT_ANIMATION:
        return

    # Prevent if new is not known
    if anim not in KNOWN_ANIMATIONS and anim != DEFAULT_ANIMATION:
        return

    loadAnimation(anim)

def setupDisplay():
    onSelectAnimation()

def loopDisplay():
    global nextFrameTime, currentFrame, currentAnimation, DEFAULT_ANIMATION

    # Wait for next frame
    if time.time() <= nextFrameTime:
        return
    nextFrameTime = time.time() + 0.15

    currentFrame += 1
    if currentFrame >= currentAnimation.getLength():

        if currentAnimation.getName() != DEFAULT_ANIMATION:
            loadAnimation(DEFAULT_ANIMATION)

        currentFrame = 0

    currentAnimation.showFrame(currentFrame, True)

    pass
