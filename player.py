#coding:utf-8
import glutils
from mesh import Mesh
from cpe3d import Object3D, Transformation3D, Text
import numpy as np
import OpenGL.GL as GL
import pyrr, time
from obstacles import Spike, Cube, Jump

class Player(Object3D):
    def __init__(self, switch):
        
        self.switch = switch
        
        m = Mesh.load_obj('ressources/meshes/cube.obj')
        m.normalize()
        
        m.apply_matrix(pyrr.matrix44.create_from_scale([0.5, 0.5, 0.5, 1]))
        
        transformation = Transformation3D()
        transformation.offset = pyrr.Vector3([0.5,0.5,0.5])
        
        texture = glutils.load_texture('ressources/textures/eliacube.png')
        
        self.bounding_box = (pyrr.Vector3([0, 0, 0]),  pyrr.Vector3([1, 0.99, 1]))
        
        transformation.translation = pyrr.Vector3([0, 0, 0])
        self.velocity = pyrr.Vector3([7, 0, 0])
        self.acceleration = pyrr.Vector3([0, -50, 0])
        
        self.onground = True
        self.moveforward = False
        self.another_chance = False
        self.prevtime = 0
        
        super().__init__(m.load_to_gpu(), m.get_nb_triangles(), texture, transformation)
        
    def set_terrain(self, terrain):
        self.terrain = terrain
    
    def tick_clock(self, dt, crttime):
        #print("-----ticked clock-----", f"{dt=}, {crttime=}")
        
        if self.onground:
            self.transformation.rotation_euler[pyrr.euler.index().pitch] = 0
        else:
            self.transformation.rotation_euler[pyrr.euler.index().pitch] += dt * 4
        
        #print('accleration',self.acceleration)
        self.velocity = self.velocity + dt * self.acceleration 
        if self.onground:
            self.velocity.y = 0
        
        #print('velocity', self.velocity)
        self.transformation.translation = self.transformation.translation + dt * self.velocity
        
        #print('position', self.transformation.translation)
        self.test_collisions()

        if self.transformation.translation.y < 0:
            #print('Ground contact')
            self.transformation.translation.y = 0
            self.transformation.rotation_euler[pyrr.euler.index().pitch] = 0
            self.onground = True
        
        #print('final position', self.transformation.translation)
        #print('-'*25)
        

    def death(self):
        print('You died')
        self.transformation.translation = pyrr.Vector3([0, 0, 0])
        self.velocity = pyrr.Vector3([7, 0, 0])
        self.onground = True
    
    def step_start(self):
        self.velocity.x = 7
        
        #print(self.transformation.translation, self.velocity, self.acceleration, self.transformation.offset, t, time.time())
    
    def jump(self):
        if self.onground:
            #self.transformation.translation.y = 0
            self.velocity.y = 17
            self.onground = False
            print('JUMPED')
    
    def longjump(self):
        self.velocity.y = 25
        self.onground = False
        print('LONG JUMPED')
    
    def test_collisions(self):
        px, py = self.transformation.translation.xy
        #print(px, py)
        #print('Near', self.terrain.get_relevant_aabb(px, py))
        #print(self.get_aabb_points())
        
        points_touched = {}
        for obj in self.terrain.get_relevant_aabb(px, py):

            points_touched[type(obj)] = []

            minpt, maxpt = obj.bounding_box
            minpt = minpt + obj.transformation.translation
            maxpt = maxpt + obj.transformation.translation
            
            #print('OBJ:', obj, obj.transformation.translation, minpt, maxpt)
            #  minpt,  pmin1, pmin2, pmin3, pmax1, pmax2, pmax3, maxpt
            for i, point in enumerate(self.get_aabb_points()):
                if minpt.x <= point.x <= maxpt.x and minpt.y <= point.y <= maxpt.y and minpt.z <= point.z <= maxpt.z:
                    points_touched[type(obj)].append(i)
            
            #print('points', points_touched)
        
        if len(points_touched) == 0:
            self.onground = False

        elif Jump in points_touched.keys():
            self.longjump()
            
        elif Cube in points_touched.keys():
            points = points_touched[Cube]
            if (7 in points) or (6 in points) or (4 in points) or (2 in points):
                self.death()
            elif (1 in points) or (5 in points) or (3 in points) or (0 in points):
                self.onground = True
                self.transformation.translation.y = maxpt.y

        elif Spike in points_touched.keys():
            self.death()

            

            

            

