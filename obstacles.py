#coding:utf-8

from click import password_option
import glutils
from mesh import Mesh
from cpe3d import Object3D, Camera, Transformation3D, Text
import numpy as np
import OpenGL.GL as GL
import pyrr

class Obstacles(Object3D):
    def __init__(self, program_id):
        
        m = Mesh.load_obj()
        m.normalize()
        m.apply_matrix(pyrr.matrix44.create_from_scale([2, 2, 2, 1]))
        tr = Transformation3D()
        tr.translation.y = -np.amin(m.vertices, axis=0)[1]
        tr.translation.z = -5
        tr.rotation_center.z = 0.2
        texture = glutils.load_texture('stegosaurus.jpg')
        super().__init__(m.load_to_gpu(), m.get_nb_triangles(), program_id, texture, tr)


class Spike(Obstacles):
    def __init__(self, x, y, z, orientation='UP'):

        if orientation == 'UP':
            pass
        elif orientation == 'LEFT':
            pass
        elif orientation == 'DOWN':
            pass
        else:
            pass


class Cube(Obstacles):
    def __init__(self, x, y, z):
        pass




if __name__ == "__main__":
    test = Level()
    test.load()