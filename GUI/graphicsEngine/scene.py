from models import *

class scene:
    def __init__(self, engine):
        self.engine=engine
        self.objects= {}
        self.load()

    def addObject(self,name,  obj):
        self.objects[name]=obj

    def load(self):
        self.addObject("Sphere1", sphere(1.0,[0.0,0.0,0.0], self.engine))

    def render(self, names, positions):
        for objName in self.objects:
            position=positions[names[objName]][0:3]
            self.objects[objName].render(position)