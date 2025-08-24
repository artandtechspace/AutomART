import json
import time
from pathlib import Path

# Config

USE_COLOR = True
DEFAULT_ANIMATION = "grinning"




# Directory where the animations are stored
animatDir = 'client/animations/'+('color' if USE_COLOR else 'nocolor')

def getKnownAnimations():
    return [p.stem for p in Path(animatDir).glob(f"*.json")]


class Animation:

    def __init__(self, name: str):
        self.__name = name

        with open(f'{animatDir}/{name}.json') as fp:
            self.__frames = json.load(fp)
    
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

def get_selected_animation():
    '''
    :return: name of the selected animation or None if the default is selected
    '''
    if currentAnimation.getName() == DEFAULT_ANIMATION:
        return None
    return currentAnimation.getName()

def loadAnimation(anim: str):
    global currentAnimation, currentFrame

    # Load animation
    currentFrame = 0
    currentAnimation = Animation(anim)

def onSelectAnimation(anim: str = DEFAULT_ANIMATION):
    global currentAnimation, DEFAULT_ANIMATION, currentFrame, currentAnimation

    # Prevent if there is an animation playing
    if currentAnimation != None and currentAnimation.getName() != DEFAULT_ANIMATION:
        return

    # Prevent if new is not known
    if anim not in getKnownAnimations() and anim != DEFAULT_ANIMATION:
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

    #currentAnimation.showFrame(currentFrame, True)
    pass
