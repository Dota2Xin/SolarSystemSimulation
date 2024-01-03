import glm

class camera:

    '''
    Creates a camera class

    Params:
    frustumParams- Array that takes in params for view frustum of [FOV, zNear, zFar]
    cameraParams- Array that takes in params for camera of [Position,center, UP]
    screenParams- Array that takes in params about screen [xWindowSize, yWindowSize]

    '''
    def __init__(self, frustumParams, cameraParams, screenParams):
        self.frustumParams=frustumParams
        self.aspectRatio=screenParams[0]/screenParams[1]
        self.position=cameraParams[0]
        self.up=cameraParams[2]
        self.center=cameraParams[1]
        self.projMatrix=glm.perspective(glm.radians(frustumParams[0]),self.aspectRatio,frustumParams[1],frustumParams[2])
        self.viewMatrix=glm.lookAt(self.position,self.center,self.up)