#coding:utf-8

import glutils
from mesh import Mesh
from cpe3d import Object3D, Transformation3D
import numpy as np
import pyrr

class Spike(Object3D):
    def __init__(self, x, y, z, orientation='UP'):
        
        
        points  = [ [0, 0, 0],  [1, 0, 0],  [0, 0, 1],     [1, 0, 1],      [0.5, 1, 0.5]]
        #normals = [ [0, 0, 1],  [0, 0, 1],  [0, 0, 1],     [0, 0, 1],      [0, 0, 1]]
        faces = [   [0,1,3],
                    [0,2,3], 
                    [0,4,2],
                    [2,4,3], 
                    [3,4,1],
                    [1,4,0] ]
        texcoords = [[0, 0],     [0, 1],       [0, 1],       [1, 1],            [0.5, 0.5]]
        n = [0,0,1]
        c = [1,1,1]
        
        
        transformation = Transformation3D()
        transformation.translation = pyrr.Vector3([x, y, z])
        
        transformation.rotation_center = pyrr.Vector3([0.5, 0.5, 0.5])
        
        if orientation == 'UP':
            transformation.rotation_euler[pyrr.euler.index().pitch] = 0
        elif orientation == 'LEFT':
            transformation.rotation_euler[pyrr.euler.index().pitch] =  np.pi / 2
        elif orientation == 'DOWN':
            transformation.rotation_euler[pyrr.euler.index().pitch] =  np.pi
        else:
            raise LevelError(f"Spike orientation not supported: {orientation}")
        
        m = Mesh()
        m.vertices = np.array([p + n + c + t for p, t in zip(points, texcoords)], np.float32)
        m.faces = np.array(faces, np.uint32)
        texture = glutils.load_texture('ressources/textures/blue_square.png')
        super().__init__(m.load_to_gpu(), m.get_nb_triangles(), texture, transformation)
        #self.wireframe = True


class Cube(Object3D):
    def __init__(self, x, y, z):
        m = Mesh.load_obj('ressources/meshes/cube.obj')
        m.normalize()
        
        m.apply_matrix(pyrr.matrix44.create_from_scale([0.5, 0.5, 0.5, 1]))
        
        transformation = Transformation3D()
        transformation.translation = pyrr.Vector3([x,y,z])
        transformation.offset = pyrr.Vector3([0.5,0.5,0.5])
        
        texture = glutils.load_texture('ressources/textures/blue_square.png')

        super().__init__(m.load_to_gpu(), m.get_nb_triangles(), texture, transformation)
        
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
        
        
