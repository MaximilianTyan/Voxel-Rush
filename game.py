#coding:utf-8
import glutils
from mesh import Mesh
from cpe3d import Object3D, Transformation3D, Text
import numpy as np
import OpenGL.GL as GL
import pyrr, time

class Player(Object3D):
    def __init__(self, program3d_id):
        m = Mesh.load_obj('ressources/meshes/stegosaurus.obj')
        m.normalize()
        m.apply_matrix(pyrr.matrix44.create_from_scale([2, 2, 2, 1]))
        texture = glutils.load_texture('ressources/textures/stegosaurus.jpg')
        
        self.velocity = pyrr.Vector3([0, 0, 0])
        self.acceleration = pyrr.Vector3([0, -70, 0])
        
        self.transformation = Transformation3D()
        self.transformation.offset.y = -np.amin(m.vertices, axis=0)[1]
        
        self.onground = False
        
        self.prevtime = 0
        super().__init__(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, self.transformation)
        
    def draw(self):
        self.tick_clock()
        super().draw()
    
    def tick_clock(self):
        crt_time = time.time()
        t = crt_time - self.prevtime
        self.prevtime = crt_time
        
        self.velocity = self.velocity + t * self.acceleration 
        self.transformation.translation = self.transformation.translation + t * self.velocity
        
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



class Wall(Object3D):
    def __init__(self, points, faces, texcoords, n=[0, 1, 0], c=[1, 1, 1], texture=None, program_id=None):
        m = Mesh()
        m.vertices = np.array([p + n + c + t for p, t in zip(points,texcoords)], np.float32)
        m.faces = np.array(faces, np.uint32)
        super().__init__(m.load_to_gpu(), m.get_nb_triangles(), program_id, texture, Transformation3D())
    
class Background():
    def __init__(self, program_id):
        # points  = [[-25, 0, -25],    [25, 0, -25],   [25, 0, 25],    [-25, 0, 25]]
        # texcoords = [[0, 0],           [1, 0],         [1, 1],         [0, 1]]
        
        texture = glutils.load_texture('ressources/textures/background.png')
        points  = [[-5, 0, 0],    [-5, 5, 0],   [5, 5, 0],    [5, 0, 0]]
        texcoords = [[0, 0],         [0, 1],       [1, 1],       [1, 0]]
        faces = [[0, 1, 2], [0, 2, 3]]
        self.backwall = Wall(points, faces, texcoords, texture=texture, program_id=program_id)
        
        self.frontwall = Wall(points, faces, texcoords, texture=texture, program_id=program_id)
        self.frontwall.transformation.offset.y = -5
        self.frontwall.transformation.offset.z = 1
        
        texture = glutils.load_texture('ressources/textures/background.png')
        points  = [[-5, 0, 1],    [-5, 0, 0],   [5, 0, 0],    [5, 0, 1]]
        texcoords = [[0, 0],         [1, 0],       [1, 1],       [0, 1]]
        faces = [[0, 1, 2], [0, 2, 3]]
        self.pathway = Wall(points, faces, texcoords, texture=texture, program_id=program_id)