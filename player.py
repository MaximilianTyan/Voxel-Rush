#coding:utf-8
import glutils
from mesh import Mesh
from cpe3d import Object3D, Transformation3D, Text
import numpy as np
import OpenGL.GL as GL
import pyrr, time
from obstacles import Spike, Cube

class Player(Object3D):
    def __init__(self):
        m = Mesh.load_obj('ressources/meshes/cube.obj')
        m.normalize()
        
        m.apply_matrix(pyrr.matrix44.create_from_scale([0.5, 0.5, 0.5, 1]))
        
        transformation = Transformation3D()
        transformation.offset = pyrr.Vector3([0.5,0.5,0.5])
        
        texture = glutils.load_texture('ressources/textures/eliacube.png')
        
        self.bounding_box = (pyrr.Vector3([0.01, 0.01, 0.01]),  pyrr.Vector3([0.99, 0.99, 0.99]))
        
        transformation.translation = pyrr.Vector3([0, 0, 0])
        self.velocity = pyrr.Vector3([0, 0, 0])
        self.acceleration = pyrr.Vector3([0, -50, 0])
        
        self.onground = True
        self.moveforward = False
        self.another_chance = False
        self.prevtime = 0
        super().__init__(m.load_to_gpu(), m.get_nb_triangles(), texture, transformation)
    
    def set_terrain(self, terrain):
        self.terrain = terrain
    
    def tick_clock(self, dt, crttime):
        
        if self.onground:
            self.transformation.rotation_euler[pyrr.euler.index().pitch] = 0
        else:
            self.transformation.rotation_euler[pyrr.euler.index().pitch] += dt * 4
        
        self.velocity = self.velocity + dt * self.acceleration 
        if self.onground:
            self.velocity.y = 0
        
        self.transformation.translation = self.transformation.translation + dt * self.velocity
        if self.transformation.translation.y < 0:
            #print('Ground contact')
            self.transformation.translation.y = 0
            self.onground = True
        
        self.test_collisions()

    def death(self):
        print('You died')
        self.transformation.translation = pyrr.Vector3([0, 0, 0])
        self.velocity = pyrr.Vector3([0, 0, 0])
        self.onground = True
    
    def step(self):
        self.velocity.x = 7
        
        #print(self.transformation.translation, self.velocity, self.acceleration, self.transformation.offset, t, time.time())
    
    def jump(self):
        if self.onground:
            #self.transformation.translation.y = 0
            self.velocity.y = 17
            self.onground = False
            print('JUMPED')
    
    def test_collisions(self):
        px, py = self.transformation.translation.xy
        #print(px, py)
        #print('Near', self.terrain.get_relevant_aabb(px, py))
        #print(self.get_aabb_points())
        
        points_touched = []
        for obj in self.terrain.get_relevant_aabb(px, py):
            minpt, maxpt = obj.bounding_box
            minpt = minpt + obj.transformation.translation
            maxpt = maxpt + obj.transformation.translation
            
            #print('OBJ:', obj, obj.transformation.translation, minpt, maxpt)
            #  minpt,  pmin1, pmin2, pmin3, pmax1, pmax2, pmax3, maxpt
            for i, point in enumerate(self.get_aabb_points()):
                if minpt.x <= point.x <= maxpt.x and minpt.y <= point.y <= maxpt.y and minpt.z <= point.z <= maxpt.z:
                    points_touched.append(i)
                    
                    if isinstance(obj, Spike):
                        self.death()
                        return
            
            #print('points', points_touched)
            
            if (7 in points_touched) or (6 in points_touched) or (4 in points_touched) or (2 in points_touched):
                self.death()
                
            elif (1 in points_touched) or (5 in points_touched) or (3 in points_touched) or (0 in points_touched):
                #print('Bottom contact')
                self.onground = True
                self.transformation.translation.y = maxpt.y - 0.01
            else:
                #print('Falling')
                self.onground = False
            
            

            

