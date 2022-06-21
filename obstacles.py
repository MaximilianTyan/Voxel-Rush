#coding:utf-8

import glutils
from mesh import Mesh
from cpe3d import Object3D, Transformation3D
import numpy as np
import pyrr
from hitbox import HitBox

def init():
    Spike.init()
    Cube.init()
    Jump.init()
    DoubleJump.init()
    print('[INIT] Obstacles classes initiated')


class Spike(Object3D):
    @classmethod
    def init(cls):
        m = Mesh.load_obj('ressources/meshes/spike.obj')
        m.normalize()
        m.apply_matrix(pyrr.matrix44.create_from_scale([0.5, 0.5, 0.5, 1]))
        
        cls.vao = m.load_to_gpu()
        cls.triangles = m.get_nb_triangles()
        
        cls.texture = glutils.load_texture('ressources/textures/red.png')
    
    def __init__(self, x, y, z, orientation='UP', /, showhitbox=False):
        
        transformation = Transformation3D()
        transformation.translation = pyrr.Vector3([x, y, z])
        transformation.offset = pyrr.Vector3([0.5, 0.5, 0.5])
        
        transformation.rotation_euler[pyrr.euler.index().roll] = -np.pi / 2
        
        if orientation == 'UP':
            transformation.rotation_euler[pyrr.euler.index().yaw] = 0
        elif orientation == 'LEFT':
            transformation.rotation_euler[pyrr.euler.index().yaw] = -np.pi / 2
        elif orientation == 'DOWN':
            transformation.rotation_euler[pyrr.euler.index().yaw] = np.pi
        else:
            raise LevelError(f"Spike orientation not supported: {orientation}")
        
        self.bounding_box =  (pyrr.Vector3([0, -0.01, 0]),  pyrr.Vector3([1, 0.7, 1]))

        super().__init__(Spike.vao, Spike.triangles, Spike.texture, transformation)
        
        self.hitbox = HitBox(self.bounding_box, [1, 0, 0])
        self.hitboxvisible = showhitbox
        


class Cube(Object3D):
    
    @classmethod
    def init(cls):
        m = Mesh.load_obj('ressources/meshes/cube.obj')
        m.normalize()
            
        m.apply_matrix(pyrr.matrix44.create_from_scale([0.5, 0.5, 0.5, 1]))
        
        cls.vao = m.load_to_gpu()
        cls.triangles = m.get_nb_triangles()
        
        cls.texture = glutils.load_texture('ressources/textures/blue_square.png')
    
    def __init__(self, x, y, z, /, showhitbox=False):
        transformation = Transformation3D()
        transformation.translation = pyrr.Vector3([x,y,z])
        transformation.offset = pyrr.Vector3([0.5, 0.5, 0.5])
        
        self.bounding_box =  (pyrr.Vector3([0, 0, 0]),  pyrr.Vector3([1, 1, 1]))
        
        super().__init__(Cube.vao, Cube.triangles, Cube.texture, transformation)
        
        self.hitbox = HitBox(self.bounding_box, [0, 1, 0])
        self.hitboxvisible = showhitbox
        
        

class Jump(Object3D):
    @classmethod
    def init(cls):
        m = Mesh.load_obj('ressources/meshes/diamond.obj')
        m.normalize()
            
        m.apply_matrix(pyrr.matrix44.create_from_scale([0.5, 1, 0.5, 1]))
        cls.vao = m.load_to_gpu()
        cls.triangles = m.get_nb_triangles()
        
        cls.texture = glutils.load_texture('ressources/textures/sun.png')
    
    def __init__(self, x, y, z, /, showhitbox=False):
        
        transformation = Transformation3D()
        transformation.translation = pyrr.Vector3([x,y,z])
        transformation.offset = pyrr.Vector3([0.5, 0, 0.5])

        self.bounding_box = (pyrr.Vector3([0,0,0]),  pyrr.Vector3([1,0.1,1]))
        
        super().__init__(Jump.vao, Jump.triangles, Jump.texture, transformation)
        self.hitbox = HitBox(self.bounding_box, [1, 1, 0])
        self.hitboxvisible = showhitbox

class DoubleJump(Object3D):
    
    @classmethod
    def init(cls):
        m = Mesh.load_obj('ressources/meshes/star.obj')
        m.normalize()
            
        m.apply_matrix(pyrr.matrix44.create_from_scale([0.3, 0.3, 0.05, 1]))
        cls.vao = m.load_to_gpu()
        cls.triangles = m.get_nb_triangles()
        
        cls.texture = glutils.load_texture('ressources/textures/sun.png')
        
        #cls.hitboxvao = s
    
    def __init__(self, x, y, z, /, showhitbox=False):
        
        transformation = Transformation3D()
        transformation.translation = pyrr.Vector3([x,y,z])
        transformation.offset = pyrr.Vector3([0.5, 0, 0.1])

        self.bounding_box = (pyrr.Vector3([0,0,0]),  pyrr.Vector3([1,0.1,1]))
        
        super().__init__(DoubleJump.vao, DoubleJump.triangles, DoubleJump.texture, transformation)
        self.hitbox = HitBox(self.bounding_box, [1, 1, 0])
        self.hitboxvisible = showhitbox
    
        """
        m = Mesh()
        points  = [ [0, 0, 0],  [1, 0, 0],  [0, 0, 1],     [1, 0, 1],      [0.5, 1, 0.5]]
        texcoords = [[0, 0],     [0, 1],       [0, 1],       [1, 1],            [0.5, 0.5]]
        
        n = [0,0,1]
        c = [1,1,1]
        
        m.vertices = np.array([p + n + c + t for p, t in zip(points, texcoords)], np.float32)
        
        faces = [   [0,1,3],
                    [0,2,3], 
                    [0,4,2],
                    [2,4,3], 
                    [3,4,1],
                    [1,4,0] ]
        m.faces = np.array(faces, np.uint32)
        """

"""
        points  = [ [0, 0, 0],  [1, 0, 0],  [0, 1, 0],   [0, 0, 1], 
                    [0, 1, 1],  [1, 0, 1],  [1, 1, 0],   [1, 1, 1] ]
        
        texcoords = [   [0, 0],     [0, 1],       [1, 1],       [1, 0],
                        [0, 0],     [0, 1],       [1, 1],       [1, 0]  ]
        
        normals = [ [0, 0, 0],  [1, 0, 0],  [0, 1, 0],   [0, 0, 1], 
                    [0, 1, 1],  [1, 0, 1],  [1, 1, 0],   [1, 1, 1] ]
        
        faces = [   [1,2,5], [1,3,5],
                    [2,6,8], [2,5,8],
                    [6,4,7], [6,8,7],
                    [4,7,3], [4,1,3],
                    [2,6,4], [2,1,4],
                    [3,5,8], [3,7,8]  ]
        
        transformation = Transformation3D()
        transformation.translation = pyrr.Vector3([x,y,z])

        m = Mesh()
        m.vertices = np.array([p + n + c + t for p, n, t in zip(points, normals, texcoords)], np.float32)
        m.faces = np.array(faces, np.uint32)
        super().__init__(m.load_to_gpu(), m.get_nb_triangles(), texture, transformation)
        """