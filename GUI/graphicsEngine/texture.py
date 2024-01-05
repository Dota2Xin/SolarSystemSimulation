import pygame as pg
import moderngl as mgl
import os

class texture:
    def __init__(self,context):
        self.ctx=context
        self.textures={}
        self.textures[0]=self.getTexture('earth1')

    def getTexture(self, name):
        currentDir = os.path.dirname(os.path.realpath(__file__))
        texture = pg.image.load(os.path.join(currentDir, f'textures/{name}.jpg')).convert()
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
        texture = self.ctx.texture(size=texture.get_size(), components=3, data=pg.image.tostring(texture, "RGB"))
        return texture

    def destroy(self):
        [tex.release() for tex in self.textures.values()]