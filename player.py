#coding:utf-8
import glutils
from mesh import Mesh
from cpe3d import Object3D, Transformation3D, Text
import numpy as np
import OpenGL.GL as GL
import pyrr, time

class Player(Object3D):
    def __init__(self):
        m = Mesh.load_obj('ressources/meshes/cube.obj')
        m.normalize()
        
        m.apply_matrix(pyrr.matrix44.create_from_scale([0.5, 0.5, 0.5, 1]))
        
        transformation = Transformation3D()
        transformation.offset = pyrr.Vector3([0.5,0.5,0.5])
        
        texture = glutils.load_texture('ressources/textures/eliacube.png')
        
        self.velocity = pyrr.Vector3([0, 0, 0])
        self.acceleration = pyrr.Vector3([0, -70, 0])
        
        self.onground = False
        
        self.prevtime = 0
        super().__init__(m.load_to_gpu(), m.get_nb_triangles(), texture, transformation)
    
    def tick_clock(self, dt, crttime):
        self.velocity = self.velocity + dt * self.acceleration 
        self.transformation.translation = self.transformation.translation + dt * self.velocity
        
        if self.onground or self.transformation.translation.y <= 0 :
            self.transformation.translation.y = 0
            self.velocity.y = 0
            self.onground = True
        
        #print(self.transformation.translation, self.velocity, self.acceleration, self.transformation.offset, t, time.time())
    
    def jump(self):
        if self.onground:
            self.velocity.y = 17
            self.onground = False
            print('JUMPED')

    

