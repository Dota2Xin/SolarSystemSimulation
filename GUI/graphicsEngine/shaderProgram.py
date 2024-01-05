import moderngl as mgl
import os

class shaderProgram:
    def __init__(self, context):
        self.ctx=context
        self.programs={}
        self.programs['sphereBasic']=self.getProgram('sphereBasic')

    def getProgram(self, shaderName):
        currentDir = os.path.dirname(os.path.realpath(__file__))

        totalPathVert = os.path.join(currentDir, f'shaders/{shaderName}.vert')
        totalPathFrag = os.path.join(currentDir, f'shaders/{shaderName}.frag')
        with open(totalPathVert) as file:
            vertexShader = file.read()
        with open(totalPathFrag) as file:
            fragmentShader = file.read()

        program = self.ctx.program(vertex_shader=vertexShader, fragment_shader=fragmentShader)
        return program

    def destroy(self):
        [program.release() for program in self.programs.values()]