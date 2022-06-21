#coding:utf-8
import glutils
from mesh import Mesh
from cpe3d import Object3D, Transformation3D, Text
import numpy as np
import OpenGL.GL as GL
import pyrr, time

class Wall(Object3D):
    def __init__(self, points, faces, texcoords, n=[0, 0, 1], c=[1, 1, 1], texture=None):
        m = Mesh()
        m.vertices = np.array([p + n + c + t for p, t in zip(points,texcoords)], np.float32)
        m.faces = np.array(faces, np.uint32)
        super().__init__(m.load_to_gpu(), m.get_nb_triangles(), texture, Transformation3D())
        self.hitbox = None
    
class Background():
    def __init__(self, camera):
        self.wall_list = []
        self.cam = camera
        
        texture = glutils.load_texture('ressources/textures/background.png')
        
        points  = [[-12, 0, 0],    [-12, 12, 0],   [12, 12, 0],    [12, 0, 0]]
        texcoords = [[0, 0],         [0, 1],       [1, 1],       [1, 0]]
        faces = [[0, 1, 2], [0, 2, 3]]
        wall = Wall(points, faces, texcoords, texture=texture)
        wall.set_name('backwall')
        self.wall_list.append(wall)
        
        frontwall = Wall(points, faces, texcoords, texture=texture)
        frontwall.transformation.offset.y = -12
        frontwall.transformation.offset.z = 1
        frontwall.set_name('frontwall')
        self.wall_list.append(frontwall)
        
        points  = [[-12, 0, 1],    [-12, 0, 0],   [12, 0, 0],    [12, 0, 1]]
        texcoords = [[0.9, 0],         [1, 0],       [1, 1],       [0.9, 1]]
        faces = [[0, 1, 2], [0, 2, 3]]
        wall = Wall(points, faces, texcoords, texture=texture)
        wall.set_name('pathway')
        self.wall_list.append(wall)
    
    def get_walls(self):
        return self.wall_list