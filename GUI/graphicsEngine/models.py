import numpy as np
import moderngl as mgl
import pygame as pg
import glm
import os

class sphere:
    '''
    Class for masking a sphere using modernGL

    Inputs:
    Radius- Float of radius of sphere
    Position- Array that looks like [x,y,z] position of center of sphere
    Name- String corresponding to name of sphere
    context- Passes the context we're currently working with
    '''
    def __init__(self, radius, position, name, engine):
        self.radius=radius
        self.position=position
        self.name=name
        self.ctx=engine.ctx
        self.engine=engine
        self.vbo=self.getVertexBuffer()
        self.shaderProgram=self.getShaderProgram('sphereBasic')
        self.vao=self.getVertexArrayObject()
        self.modelMatrix=glm.mat4(1,0,0,0, 0,1,0,0, 0,0,1,0, position[0],position[1],position[2],1)
        self.texture=self.getTexture("earth1")
        self.onInit()

    def onInit(self):
        #texture
        self.shaderProgram['u_texture_0']=0
        self.texture.use()
        #viewing
        self.shaderProgram['m_proj'].write(self.engine.camera.projMatrix)
        self.shaderProgram['m_view'].write(self.engine.camera.viewMatrix)
        self.shaderProgram['m_model'].write(self.modelMatrix)


    def update(self, position):
        self.modelMatrix= glm.mat4(1,0,0,0, 0,1,0,0, 0,0,1,0, position[0],position[1],position[2],1)
        self.shaderProgram['m_model'].write(self.modelMatrix)
        self.shaderProgram['m_proj'].write(self.engine.camera.projMatrix)
        self.shaderProgram['m_view'].write(self.engine.camera.viewMatrix)

    def render(self):
        self.vao.render()

    def destroy(self):
        self.vbo.release()
        self.shaderProgram.release()
        self.vao.release()

    def getTexture(self, name):
        currentDir = os.path.dirname(os.path.realpath(__file__))
        texture=pg.image.load(os.path.join(currentDir,f'textures/{name}.jpg')).convert()
        texture=pg.transform.flip(texture,flip_x=False,flip_y=True)
        texture=self.ctx.texture(size=texture.get_size(),components=3,data=pg.image.tostring(texture, "RGB"))
        return texture

    #calculates the locations of the vertices and the value of the vertex normals at every point and reuturns them
    #in format vertex, normal
    def getVertexArray(self):
        #sets the resolution of the spheres from a 3D standpoint
        latitudeSegments=32
        longitudeSegments=32

        vertex=[]
        textureCoords=[]

        #do the calculation: Note: In spherical polar coordinates
        for i in range(latitudeSegments+1):
            if i!=0 and i!=latitudeSegments:
                for j in range(longitudeSegments+1):
                    theta=np.pi*i*1.0/latitudeSegments
                    phi=2*np.pi*j*1.0/longitudeSegments

                    xNorm=np.sin(theta)*np.cos(phi)
                    yNorm=np.sin(theta)*np.sin(phi)
                    zNorm=np.cos(theta)

                    x=xNorm*self.radius
                    y = yNorm * self.radius
                    z = zNorm * self.radius

                    vertex.append([x,y,z])
                    textureCoords.append([j*1.0/longitudeSegments, i*1.0/latitudeSegments])
            else:
                theta = np.pi * i * 1.0 / latitudeSegments
                z=np.cos(theta)*self.radius
                vertex.append([0,0,z])
                textureCoords.append([0,i*1.0/latitudeSegments])

        indices=[]

        for i in range(latitudeSegments):
            if i!=0 and i!=latitudeSegments-1:
                zeroIndex=(i-1)*32+1
                for j in range(longitudeSegments):
                    triangle1=(zeroIndex+j,zeroIndex+j+32,zeroIndex+(j+1)%longitudeSegments)
                    triangle2=(zeroIndex+j+32,zeroIndex+32+(j+1)%longitudeSegments,zeroIndex+(j+1)%longitudeSegments)
                    indices.append(triangle1)
                    indices.append(triangle2)
            else:
                if i==0:
                    for j in range(latitudeSegments):
                        triangle=(0,1+j,1+(j+1)%longitudeSegments)
                        indices.append(triangle)
                else:
                    zeroIndex = (i - 1) * 32 + 1
                    for j in range(latitudeSegments):
                        triangle=(zeroIndex+j,zeroIndex+(j+1)%longitudeSegments,len(vertex)-1)
                        indices.append(triangle)

        return self.getData(vertex,textureCoords, indices)


    @staticmethod
    def getData(vertices,textureCoords, indices):
        vertexData=[vertices[ind]+textureCoords[ind] for triangle in indices for ind in triangle]
        return np.array(vertexData,dtype='f4')

    def getVertexBuffer(self):
        vertexData=self.getVertexArray()
        #vbo=self.ctx.buffer(np.concatenate([vertexData[0],vertexData[1]]))
        vbo = self.ctx.buffer(vertexData)
        return vbo

    def getVertexArrayObject(self):
        vao=self.ctx.vertex_array(self.shaderProgram, [(self.vbo,'3f 2f','in_position', "in_texcoord_0")])
        return vao

    def getShaderProgram(self, shaderName):
        currentDir=os.path.dirname(os.path.realpath(__file__))

        totalPathVert=os.path.join(currentDir,f'shaders/{shaderName}.vert')
        totalPathFrag=os.path.join(currentDir,f'shaders/{shaderName}.frag')
        with open(totalPathVert) as file:
            vertexShader=file.read()
        with open(totalPathFrag) as file:
            fragmentShader=file.read()

        program=self.ctx.program(vertex_shader=vertexShader, fragment_shader=fragmentShader)
        return program
