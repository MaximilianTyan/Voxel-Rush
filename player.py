#coding:utf-8
import glutils
from mesh import Mesh
from cpe3d import Object3D, Transformation3D, Text
import numpy as np
import OpenGL.GL as GL
import pyrr, time
from obstacles import Spike, Cube, Jump, DoubleJump
from hitbox import HitBox

class Player(Object3D):
    def __init__(self, switch):
        
        self.switch = switch
        
        m = Mesh.load_obj('ressources/meshes/cube.obj')
        m.normalize()
        
        m.apply_matrix(pyrr.matrix44.create_from_scale([0.5, 0.5, 0.5, 1]))
        
        transformation = Transformation3D()
        transformation.offset = pyrr.Vector3([0.5,0.5,0.5])
        
        texture = glutils.load_texture('ressources/textures/eliacube.png')
        
        self.bounding_box = (pyrr.Vector3([0.01, 0, 0.01]),  pyrr.Vector3([0.99, 0.98, 0.99]))
        
        transformation.translation = pyrr.Vector3([0, 0, 0])
        self.velocity = pyrr.Vector3([0, 0, 0])
        self.acceleration = pyrr.Vector3([0, 0, 0])
        
        
        self.onground = True
        self.can_double_jump = False
        super().__init__(m.load_to_gpu(), m.get_nb_triangles(), texture, transformation)
        
        self.hitbox = HitBox(self.bounding_box, [1, 1, 1])
        self.hitboxvisible = False
        self.wireframe = False
        self.deathcount = 0
        
        self.reset()
        
    
    def reset(self):
        self.transformation.translation = pyrr.Vector3([0, 0, 0])
        self.transformation.rotation_euler = pyrr.euler.create()
        self.velocity = pyrr.Vector3([0, 0, 0])
        self.acceleration = pyrr.Vector3([0, -100, 0])
        
        self.onground = True
        self.can_double_jump = False
        self.deathcount = 0
        print('[PLAYER] Player reseted')
        print('[PLAYER] Initial acceleration vector:', self.acceleration)
    
    def set_sound(self, sound):
        self.sound_manager = sound
        self.sound_manager.load_sound('death', 'geometry-dash-death-sound-effect.mp3')
    
    def set_terrain(self, terrain):
        self.terrain = terrain
    
    def tick_clock(self, dt, crttime):
        #print("-----ticked clock-----", f"{dt=}, {crttime=}")
        #prev_pos = self.transformation.translation
        
        if self.onground:
            self.transformation.rotation_euler[pyrr.euler.index().pitch] = 0
        else:
            self.transformation.rotation_euler[pyrr.euler.index().pitch] += dt * 4
        
        #print('accleration',self.acceleration)
        self.velocity = self.velocity + dt * self.acceleration 
        if self.onground:
            self.velocity.y = 0
        if self.velocity.y < -25.5:
            self.velocity.y = -25.5
        
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
        #print('deplacement', self.transformation.translation - prev_pos)

    def death(self):
        print('[PLAYER] You died')
        self.sound_manager.sounds['death'].play()
        self.sound_manager.restart_music()
        self.transformation.translation = pyrr.Vector3([0, 0, 0])
        self.transformation.rotation = pyrr.euler.create()
        self.step_start()
        self.onground = True
        self.deathcount += 1
    
    def step_start(self):
        self.velocity.x = 10
        
        #print(self.transformation.translation, self.velocity, self.acceleration, self.transformation.offset, t, time.time())
    
    def jump(self):
        if self.onground or self.can_double_jump:
            #self.transformation.translation.y = 0
            self.velocity.y = 25.5
            self.onground = False
            
            if self.can_double_jump:
                print("[PLAYER] DOUBLE JUMPED")
                self.can_double_jump = False
            else:
                print('[PLAYER] JUMPED')
    
    def longjump(self):
        self.velocity.y = 35
        self.onground = False
        print('[PLAYER] LONG JUMPED')
    
    def test_collisions(self, hasSpareChance=True):
        points_touched = self.check_points()
        #print(points_touched)
        if points_touched == [None]*8:
            self.onground = False
            self.can_double_jump = False
            return
        
        #(1,4,2,6) bottom points
        #(3,5,7,8) top points
        #print(points_touched)
        
        for i in (5,8): #(3,5,7,8) top points
            obj = points_touched[i-1]
            if isinstance(obj, DoubleJump):
                self.can_double_jump = True
            if isinstance(obj, Cube):
                print('[PLAYER] Top collision with Cube')
                self.death()
                return
            elif isinstance(obj, Spike):
                print('[PLAYER] Top collision with Spike')
                self.death()
                return
        
        
        recheck = False
        for i in (4,6): #(1,4,2,6) bottom points
            obj = points_touched[i-1]
            
            if isinstance(obj, DoubleJump):
                self.can_double_jump = True
                
            if isinstance(obj, Jump):
                self.longjump()
                return
                
            elif isinstance(obj, Cube):
                if abs(obj.transformation.translation.y - self.transformation.translation.y) >= 1 -0.8:
                    self.onground = True
                    self.transformation.translation.y = obj.transformation.translation.y + obj.bounding_box[1].y
                    #print('Avoided front collision')
                    recheck = True
                else:
                    print('[PLAYER] Front collision with Cube')
                    self.death()
                    return
            
            if isinstance(obj, Spike):
                if recheck and hasSpareChance:
                    self.test_collisions(hasSpareChance=False)
                else:
                    self.death()
                    return

    
    def check_points(self):
        px, py = self.transformation.translation.xy
        
        #print('position', px, py)
        #print('Near', self.terrain.get_near_obstacles(px, py))
        #print(self.get_aabb_points())
        
        points_touched = [None]*8
        for obj in self.terrain.get_near_obstacles(px, py):
            minpt, maxpt = obj.bounding_box
            minpt = minpt + obj.transformation.translation
            maxpt = maxpt + obj.transformation.translation
            
            for i, point in enumerate(self.get_aabb_points()):
                if minpt.x <= point.x <= maxpt.x and minpt.y <= point.y <= maxpt.y and minpt.z <= point.z <= maxpt.z:
                    #print(i, obj, minpt, maxpt, point)
                    if not isinstance(points_touched[i], Cube) and (points_touched[i] != None):
                        #print('Continued', obj)
                        continue
                    points_touched[i] = obj
                    
        return points_touched