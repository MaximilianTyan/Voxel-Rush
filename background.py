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
    
class Background():
    def __init__(self, camera):
        # points  = [[-25, 0, -25],    [25, 0, -25],   [25, 0, 25],    [-25, 0, 25]]
        # texcoords = [[0, 0],           [1, 0],         [1, 1],         [0, 1]]
        self.wall_list = []
        self.cam = camera
        
        texture = glutils.load_texture('ressources/textures/background.png')
        points  = [[-5, 0, 0],    [-5, 5, 0],   [5, 5, 0],    [5, 0, 0]]
        texcoords = [[0, 0],         [0, 1],       [1, 1],       [1, 0]]
        faces = [[0, 1, 2], [0, 2, 3]]
        self.wall_list.append(Wall(points, faces, texcoords, texture=texture))
        
        frontwall = Wall(points, faces, texcoords, texture=texture)
        frontwall.transformation.offset.y = -5
        frontwall.transformation.offset.z = 1
        self.wall_list.append(frontwall)
        
        texture = glutils.load_texture('ressources/textures/background.png')
        points  = [[-5, 0, 1],    [-5, 0, 0],   [5, 0, 0],    [5, 0, 1]]
        texcoords = [[0, 0],         [1, 0],       [1, 1],       [0, 1]]
        faces = [[0, 1, 2], [0, 2, 3]]
        self.wall_list.append(Wall(points, faces, texcoords, texture=texture))
    
    def get_walls(self):
        return self.wall_list