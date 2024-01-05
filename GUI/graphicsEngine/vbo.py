import moderngl as mgl
import numpy as np
import glm
import pygame as pg

class vbo:
    def __init__(self, context):
        self.vbos={}
        self.vbos['sphere']=sphereVbo(context,1.0)

    def destroy(self):
        [vbo.destroy() for vbo in self.vbos.values()]

class sphereVbo:
    def __init__(self, context, radius):
        self.ctx=context
        self.radius=radius
        self.vbo=self.getVertexBuffer()
        self.format='3f 2f'
        self.attrib= ['in_position', "in_texcoord_0"]

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

    def destroy(self):
        self.vbo.release()