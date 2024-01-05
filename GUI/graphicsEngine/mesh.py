from .texture import texture
from .vao import vao

class mesh:
    def __init__(self, context):
        self.ctx=context
        self.vao=vao(context)
        self.texture=texture(context)

    def destroy(self):
        self.vao.destroy()
        self.texture.destroy()