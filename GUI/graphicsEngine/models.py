import numpy as np
import moderngl as mgl
import pygame as pg
import glm
import os

#textures are from https://www.solarsystemscope.com/textures/

class sphere:
    '''
    Class for masking a sphere using modernGL

    Inputs:
    Radius- Float of radius of sphere
    Position- Array that looks like [x,y,z] position of center of sphere
    Name- String corresponding to name of sphere
    context- Passes the context we're currently working with
    '''
    def __init__(self, radius, position, engine,omega=0,textureUnit=0, textureName="earth", resolution=64):
        self.radius=radius
        self.omega=omega
        self.position=position
        self.ctx=engine.ctx
        self.resolution=resolution
        self.engine=engine
        self.vbo=self.getVertexBuffer()
        self.shaderProgram=self.getShaderProgram('sphereBasic')
        self.vao=self.getVertexArrayObject()
        self.modelMatrix=glm.mat4(1,0,0,0, 0,1,0,0, 0,0,1,0, position[0],position[1],position[2],1)
        self.texture=self.getTexture(textureName)
        self.onInit(textureUnit)

    def onInit(self, textureUnit):
        #texture
        self.shaderProgram['u_texture_0']=textureUnit
        self.texture.use(textureUnit)
        #viewing
        self.shaderProgram['m_proj'].write(self.engine.camera.projMatrix)
        self.shaderProgram['m_view'].write(self.engine.camera.viewMatrix)
        self.shaderProgram['m_model'].write(self.modelMatrix)


    def update(self, position, deltaT):
        self.position=position
        self.modelMatrix= glm.mat4(1,0,0,0, 0,1,0,0, 0,0,1,0, position[0],position[1],position[2],1)
        self.modelMatrix=glm.rotate(self.modelMatrix, self.omega*deltaT, glm.vec3(0,0,1))
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
        texture=pg.transform.flip(texture,flip_x=False,flip_y=False)
        texture=self.ctx.texture(size=texture.get_size(),components=3,data=pg.image.tostring(texture, "RGB"))
        return texture

    #calculates the locations of the vertices and the value of the vertex normals at every point and reuturns them
    #in format vertex, normal
    def getVertexArray(self):
        #sets the resolution of the spheres from a 3D standpoint
        latitudeSegments=self.resolution
        longitudeSegments=self.resolution

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
                zeroIndex=(i-1)*latitudeSegments+1
                for j in range(longitudeSegments):
                    triangle1=(zeroIndex+j,zeroIndex+j+latitudeSegments,zeroIndex+(j+1)%longitudeSegments)
                    triangle2=(zeroIndex+j+latitudeSegments,zeroIndex+latitudeSegments+(j+1)%longitudeSegments,zeroIndex+(j+1)%longitudeSegments)
                    indices.append(triangle1)
                    indices.append(triangle2)
            else:
                if i==0:
                    for j in range(latitudeSegments):
                        triangle=(0,1+j,1+(j+1)%longitudeSegments)
                        indices.append(triangle)
                else:
                    zeroIndex = (i - 1) * latitudeSegments + 1
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

class cube:
    '''
        Class for masking a sphere using modernGL

        Inputs:
        Radius- Float of radius of sphere
        Position- Array that looks like [x,y,z] position of center of sphere
        Name- String corresponding to name of sphere
        context- Passes the context we're currently working with
        '''

    def __init__(self, sideLength, position, engine, textureUnit=0, textureName="earth", resolution=100):
        self.sideLength = sideLength
        self.position = position
        self.ctx = engine.ctx
        self.resolution = resolution
        self.engine = engine
        self.vbo = self.getVertexBuffer()
        self.shaderProgram = self.getShaderProgram('sphereBasic')
        self.vao = self.getVertexArrayObject()
        self.modelMatrix = glm.mat4(1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, position[0], position[1], position[2], 1)
        self.texture = self.getTexture(textureName)
        self.onInit(textureUnit)

    def onInit(self, textureUnit):
        # texture
        self.shaderProgram['u_texture_0'] = textureUnit
        self.texture.use(textureUnit)
        # viewing
        self.shaderProgram['m_proj'].write(self.engine.camera.projMatrix)
        self.shaderProgram['m_view'].write(self.engine.camera.viewMatrix)
        self.shaderProgram['m_model'].write(self.modelMatrix)

    def update(self, position):
        self.position = position
        self.modelMatrix = glm.mat4(1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, position[0], position[1], position[2], 1)
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
        texture = pg.image.load(os.path.join(currentDir, f'textures/{name}.jpg')).convert()
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
        texture = self.ctx.texture(size=texture.get_size(), components=3, data=pg.image.tostring(texture, "RGB"))
        return texture

    # calculates the locations of the vertices and the value of the vertex normals at every point and reuturns them
    # in format vertex, normal
    def getVertexArray(self):
        a=self.sideLength
        vertex=[(-a,-a,a),(a,-a,a),(a,a,a),(-a,a,a,),(-a,a,-a),(-a,-a,-a), (a,-a,-a), (a,a,-a)]

        indices=[(0,2,3),(0,1,2),(1,7,2),(1,6,7),(6,5,4),(4,7,6),(3,4,5),(3,5,0),(3,7,4),(3,2,7),(0,6,1),(0,5,6)]
        textureCoordinates=[(0,0),(1,0),(1,1),(0,1)]
        textureCoordIndex=[(0,2,3),(0,1,2),(0,2,3),(0,1,2),(0,1,2),(2,3,0),(2,3,0),(2,0,1),(0,2,3),(0,1,2),(3,1,2),(3,0,1)]

        textureData=self.getData(textureCoordinates,textureCoordIndex)
        vertexData=self.getData(vertex, indices)

        fullData=np.hstack([vertexData, textureData])
        return fullData

    @staticmethod
    def getData(vertices, indices):
        vertexData=[vertices[ind] for triangle in indices for ind in triangle]
        return np.array(vertexData, dtype='f4')

    def getVertexBuffer(self):
        vertexData = self.getVertexArray()
        # vbo=self.ctx.buffer(np.concatenate([vertexData[0],vertexData[1]]))
        vbo = self.ctx.buffer(vertexData)
        return vbo

    def getVertexArrayObject(self):
        vao = self.ctx.vertex_array(self.shaderProgram, [(self.vbo, '3f 2f', 'in_position', "in_texcoord_0")])
        return vao

    def getShaderProgram(self, shaderName):
        currentDir = os.path.dirname(os.path.realpath(__file__))

        totalPathVert = os.path.join(currentDir, f'shaders/{shaderName}.vert')
        totalPathFrag = os.path.join(currentDir, f'shaders/{shaderName}.frag')
        with open(totalPathVert) as file:
            vertexShader = file.read()
        with open(totalPathFrag) as file:
            fragmentShader = file.read()

        program = self.ctx.program(vertex_shader=vertexShader, fragment_shader=fragmentShader)
        return program

class ring:
    '''
    Class for masking a Ring using modernGL

    Inputs:
    Radius- Float of radius of sphere
    Position- Array that looks like [x,y,z] position of center of sphere
    Name- String corresponding to name of sphere
    context- Passes the context we're currently working with
    decorate- Rings are decorators meaning they decorate some initial object and use that to update their qualities
    '''
    def __init__(self, radiusInner, radiusOuter, position, engine, decorate,textureUnit=0, textureName="saturnsrings", resolution=64):
        self.radiusInner=radiusInner
        self.radiusOuter=radiusOuter
        self.position=position
        self.ctx=engine.ctx
        self.resolution=resolution
        self.decorate=decorate
        self.engine=engine
        self.vbo=self.getVertexBuffer()
        self.shaderProgram=self.getShaderProgram('sphereBasic')
        self.vao=self.getVertexArrayObject()
        self.modelMatrix=glm.mat4(1,0,0,0, 0,1,0,0, 0,0,1,0, position[0],position[1],position[2],1)
        self.texture=self.getTexture(textureName)
        self.onInit(textureUnit)

    def onInit(self, textureUnit):
        #texture
        self.shaderProgram['u_texture_0']=textureUnit
        self.texture.use(textureUnit)
        #viewing
        self.shaderProgram['m_proj'].write(self.engine.camera.projMatrix)
        self.shaderProgram['m_view'].write(self.engine.camera.viewMatrix)
        self.shaderProgram['m_model'].write(self.modelMatrix)


    def update(self):
        position=self.decorate.position
        self.position=position
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
        texture=pg.transform.flip(texture,flip_x=False,flip_y=False)
        texture=self.ctx.texture(size=texture.get_size(),components=3,data=pg.image.tostring(texture, "RGB"))
        return texture

    #calculates the locations of the vertices and the value of the vertex normals at every point and reuturns them
    #in format vertex, normal
    def getVertexArray(self):
        #sets the resolution of the spheres from a 3D standpoint
        segments=self.resolution

        vertex=[]
        textureCoords=[]

        #do the calculation: Note: In spherical polar coordinates
        for i in range(segments):
            deltaTheta=2*np.pi/segments
            theta=i*deltaTheta
            x=self.radiusInner*np.cos(theta)
            y=self.radiusInner*np.sin(theta)
            vertex.append([x,y,0])
            textureCoords.append([0.0, 0.0])

            x = self.radiusOuter * np.cos(theta)
            y = self.radiusOuter * np.sin(theta)
            vertex.append([x, y, 0])
            textureCoords.append([1.0, 0.0])

        indices=[]

        for i in range(2*segments):
            if i!=2*segments-1 and i!=2*segments-2:
                if i%2==0:
                    triangle=(i,i+1,i+2)
                else:
                    triangle=(i,i+2,i+1)
                indices.append(triangle)
            else:
                if i==2*segments-1:
                    triangle=(i,1,0)
                    indices.append(triangle)
                else:
                    triangle=(i,i+1,0)
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