import glm
import pygame as pg

class camera:

    '''
    Creates a camera class

    Params:
    frustumParams- Array that takes in params for view frustum of [FOV, zNear, zFar]
    cameraParams- Array that takes in params for camera of [Position,center, UP]
    screenParams- Array that takes in params about screen [xWindowSize, yWindowSize]
    movementParams- Array that takes in params about movement [Speed, sensitivity]

    '''
    def __init__(self, frustumParams, cameraParams, screenParams, speedParams, pitch=0, yaw=-90):
        self.frustumParams=frustumParams
        self.width=screenParams[0]
        self.aspectRatio=screenParams[0]/screenParams[1]
        self.position=glm.vec3(cameraParams[0][0],cameraParams[0][1],cameraParams[0][2])
        self.up=cameraParams[2]
        self.center=cameraParams[1]

        #orientation commands
        self.pitch=pitch
        self.yaw=yaw

        #camera basis vectors
        self.forward = glm.vec3(0, 0, -1)
        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)

        self.projMatrix=glm.perspective(glm.radians(frustumParams[0]),self.aspectRatio,frustumParams[1],frustumParams[2])
        self.viewMatrix=glm.lookAt(self.position,self.position+self.forward,self.up)
        self.speed=speedParams[0]
        self.sensitivity=speedParams[1]

    #updates the camera with the game clock, dt is just time difference between frames
    def update(self, dt):
        self.move(dt)
        self.rotate()
        self.viewMatrix=glm.lookAt(self.position,self.position+self.forward,self.up)
        pg.mouse.set_pos(self.width/2, self.width/(2*self.aspectRatio))


    def rotate(self):
        mouse=pg.mouse.get_pressed()
        #  if mouse[1]:
        movement=pg.mouse.get_rel()
        #angle to rotate around z-axis of up vector
        self.yaw+=movement[0]*self.sensitivity
        #angle to rotate around x-axis of right vector
        self.pitch-=movement[1]*self.sensitivity
        self.pitch=max(-89,min(89,self.pitch))
        self.setBasisVectors()
        #else:
            #quickUpdate = pg.mouse.get_rel()

    def setBasisVectors(self):
        yaw, pitch=glm.radians(self.yaw), glm.radians(self.pitch)

        self.forward.x=glm.cos(yaw)*glm.cos(pitch)
        self.forward.z=glm.sin(yaw)*glm.cos(pitch)
        self.forward.y=glm.sin(pitch)

        self.forward=glm.normalize(self.forward)
        self.right=glm.normalize(glm.cross(self.forward,glm.vec3(0,1,0)))
        self.up=glm.normalize(glm.cross(self.right,self.forward))

    def move(self, dt):
        deltaX=dt*self.speed
        keys=pg.key.get_pressed()
        if keys[pg.K_w]:
            self.position += self.forward*deltaX #-= cause z is reversed in openGL
            #self.center[2] -=deltaX
        if keys[pg.K_s]:
            self.position -=self.forward*deltaX
            #self.center[2] +=deltaX
        if keys[pg.K_a]:
            self.position -=self.right*deltaX
            #self.center[0] -=deltaX
        if keys[pg.K_d]:
            self.position +=self.right*deltaX
            #self.center[0] +=deltaX
        if keys[pg.K_SPACE]:
            self.position +=self.up*deltaX
            #self.center[1]+=deltaX
        if keys[pg.K_LSHIFT]:
            self.position -=self.up*deltaX
            #self.center[1]-=deltaX



