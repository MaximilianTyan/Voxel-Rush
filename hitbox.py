#coding:utf-8

import glutils
from mesh import Mesh
from cpe3d import Object3D, Transformation3D
import numpy as np
import pyrr

def init():
    HitBox.init()
    print('[INIT] Hitbox class initiated')

class HitBox(Object3D):
    def __init__(self, bounding_box, color):
        m = Mesh()
        #print('HITBOX:', bounding_box, color)
        minpt, maxpt = bounding_box
        delta = maxpt - minpt
        
        pmin1 = minpt + delta * [1, 0, 0]
        pmin2 = minpt + delta * [0, 1, 0]
        pmin3 = minpt + delta * [0, 0, 1]
        
        pmax1 = maxpt - delta * [1, 0, 0]
        pmax2 = maxpt - delta * [0, 1, 0]
        pmax3 = maxpt - delta * [0, 0, 1]
        
        pts = [list(p) for p in (minpt,  pmin1, pmin2, pmin3, pmax1, pmax2, pmax3, maxpt)]
        #print(pts)
        nls = [     [-1,-1,-1], 
                    [ 1,-1,-1], 
                    [-1, 1,-1], 
                    [-1,-1, 1], 
                    [-1, 1, 1], 
                    [ 1,-1, 1], 
                    [ 1, 1,-1], 
                    [ 1, 1, 1] ]
        t = [0.5, 0.5]
        
        # print(pts, nls, color, t)
        # print([pts[i] + nls[i] + color + t for i in range(len(pts))])
        m.vertices = np.array(
            [p + n + color + t for p,n in zip(pts, nls)],
            np.float32)
        
        faces = [   [1-1,2-1,6-1],    [1-1,4-1,6-1],
                    [1-1,4-1,5-1],    [1-1,3-1,5-1],
                    [1-1,2-1,7-1],    [1-1,3-1,7-1],
                    [4-1,5-1,8-1],    [4-1,6-1,8-1],
                    [2-1,7-1,8-1],    [2-1,6-1,8-1],
                    [3-1,5-1,8-1],    [3-1,7-1,8-1]]
        
        m.faces = np.array(faces, np.uint32)
        
        super().__init__(m.load_to_gpu(), m.get_nb_triangles(), HitBox.texture)
        self.wireframe = True
        self.transformation.offset.z = 0.01
    
    @classmethod
    def init(cls):
        cls.texture = glutils.load_texture('ressources/textures/white.png')