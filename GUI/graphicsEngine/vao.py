from vbo import vbo
from shaderProgram import shaderProgram


class vao():
    def __init__(self, context):
        self.ctx=context
        self.vbo=vbo(context)
        self.program=shaderProgram(context)
        self.vaos={}

        self.vaos["Sphere1"]=self.getVao(program=self.program.programs['sphereBasic'],vbo=self.vbo.vbos['sphere'])

    def getVao(self, program, vbo):
        vao = self.ctx.vertex_array(program, [(vbo.vbo, vbo.format, *vbo.attribs)])
        return vao

    def destroy(self):
        self.vbo.destroy()
        self.program.destroy()