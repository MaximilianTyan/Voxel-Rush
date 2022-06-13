#!/usr/bin/env python3

import OpenGL.GL as GL
import glfw
import pyrr
import numpy as np
import time
import ctypes

from cpe3d import Object3D
from reflist import reflist

class ViewerGL:
    def __init__(self, switch):
        
        self.switch = switch
        
        # initialisation de la librairie GLFW
        glfw.init()
        # paramétrage du context OpenGL
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        # création et paramétrage de la fenêtre
        glfw.window_hint(glfw.RESIZABLE, False)
        self.window = glfw.create_window(1600, 900, 'OpenGL', None, None)
        
        glfw.set_key_callback(self.window, self.key_callback)
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)
        GL.glEnable(GL.GL_DEPTH_TEST)
        
        GL.glClearColor(0.5, 0.6, 0.9, 1.0)
        print(f"OpenGL: {GL.glGetString(GL.GL_VERSION).decode('ascii')}")

        self.prevtime = 0
        self.background = []
        self.clocked_objs= []
        self.objs = {'common':reflist()}
        self.touch = {}

    def run(self):
        print('camera:', self.cam)
        print('background:', self.background)
        
        print('objs:', self.objs)
        print('clocked:', self.clocked_objs)
        
        # boucle d'affichage
        while not glfw.window_should_close(self.window):
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

            self.update_key()
            
            if self.switch[0] == 'level':
                crt_time = glfw.get_time()
                dt = crt_time - self.prevtime
                self.prevtime = crt_time
                
                for obj in self.clocked_objs:
                    obj.tick_clock(dt, crt_time)
            
            # Camera follow player
            player_pos = self.objs['common']['player'].transformation.translation.xyz
            cam_offset = pyrr.Vector3([3,-5,10])
            #if player_pos.y - self.cam.transformation.translation > :
            #    cam_offset.y = 3
            
            cam_center = player_pos + cam_offset
            
            self.cam.transformation.translation = cam_center
            self.cam.transformation.rotation_center = cam_center
            
            # Background follows camera
            for wall in self.background:
                wall.transformation.translation.x = self.cam.transformation.translation.x
            
            #print('cam pos:\t', self.cam.transformation.translation.xyz)
            #print('player pos:\t', self.objs['common']['player'].transformation.translation.xyz)
            #print('wall pos:\t', self.background[0].transformation.translation.xyz)
            
            #print('### LIST OBJS:', self.background, self.objs[self.switch[0]], self.objs['common'])
            for obj in self.background + self.objs[self.switch[0]] + self.objs['common']:
                if obj.visible:
                    if obj.program is None: 
                        raise Exception(f"Le programme de rendu n'a pas été précisé : {obj.program} at {obj}")
                    GL.glUseProgram(obj.program)

                    if isinstance(obj, Object3D):
                        self.update_camera(obj.program)
                    obj.draw()

                    if obj.hitboxvisible:
                        self.draw_box(obj.get_aabb_points())

            # changement de buffer d'affichage pour éviter un effet de scintillement
            glfw.swap_buffers(self.window)
            # gestion des évènements
            glfw.poll_events()
            
            #raise Exception("Stopping program for debugging")

    
    def key_callback(self, win, key, scancode, action, mods):
        # sortie du programme si appui sur la touche 'échappement'
        self.window = win
        self.touch[key] = action
    
    def add_object(self, category, obj):
        if category not in self.objs.keys():
            self.objs[category] = []
        if isinstance(obj, list) or isinstance(obj, tuple):
            for o in obj:
                self.objs[category].append(o)
        else:
            self.objs[category].append(obj)
    
    def add_ref_object(self, ref, obj):
        self.objs['common'].refappend(ref, obj)
    
    def add_clocked_object(self, obj):
        self.clocked_objs.append(obj)
    
    def set_background(self, obj):
        if isinstance(obj, list) or isinstance(obj, tuple):
            for o in obj:
                self.background.append(o)
        else:
            self.background.append(obj)

    def set_camera(self, cam):
        self.cam = cam
    
    def draw_box(self, points):
        minpt,  pmin1, pmin2, pmin3, pmax1, pmax2, pmax3, maxpt = points
        for pt in (points[1], points[2], points[3]):
            self.draw_line(points[0], pt)
        for pt in (points[-4], points[-3], points[-2]):
            self.draw_line(points[-1], pt)

    def draw_line(self, pt1, pt2, color=(0, 0, 0)):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        GL.glDrawElements(GL.GL_LINES, 2, GL.GL_UNSIGNED_INT, None)

    def update_camera(self, prog):
        GL.glUseProgram(prog)
        loc = GL.glGetUniformLocation(prog, "translation_view")
        translation = -self.cam.transformation.translation
        GL.glUniform4f(loc, translation.x, translation.y, translation.z, 0)

        loc = GL.glGetUniformLocation(prog, "offset_view")
        offset = -self.cam.transformation.offset
        GL.glUniform4f(loc, offset.x, offset.y, offset.z, 0)
        
        loc = GL.glGetUniformLocation(prog, "rotation_center_view")
        rotation_center = self.cam.transformation.rotation_center
        GL.glUniform4f(loc, rotation_center.x, rotation_center.y, rotation_center.z, 0)

        rot = pyrr.matrix44.create_from_eulers(-self.cam.transformation.rotation_euler)
        loc = GL.glGetUniformLocation(prog, "rotation_view")
        GL.glUniformMatrix4fv(loc, 1, GL.GL_FALSE, rot)
    
        loc = GL.glGetUniformLocation(prog, "projection")
        GL.glUniformMatrix4fv(loc, 1, GL.GL_FALSE, self.cam.projection)

    def update_key(self):
        
        if self.switch[0] == 'level':
            if glfw.KEY_SPACE in self.touch and self.touch[glfw.KEY_SPACE] > 0:
                self.objs['common']['player'].jump()
            if glfw.KEY_S in self.touch and self.touch[glfw.KEY_S] > 0:
                self.objs['common']['player'].step_start()
            
            if glfw.KEY_R in self.touch and self.touch[glfw.KEY_R] > 0:
                self.objs['common']['player'].death()
                
            if glfw.KEY_ESCAPE in self.touch and self.touch[glfw.KEY_ESCAPE] > 0:
                self.switch[0] = 'title'
        
        elif self.switch[0] == 'title':
            if glfw.KEY_ESCAPE in self.touch and self.touch[glfw.KEY_ESCAPE] > 0:
                glfw.set_window_should_close(self.window, glfw.TRUE)
            if glfw.KEY_S in self.touch and self.touch[glfw.KEY_S] > 0:
                print('='*20 + 'Started level' + '='*20)
                #self.objs['common']['player'].step_start()
                self.switch[0] = 'level'
                glfw.set_time(0)
                #self.objs['common']['player'].death()
        
        if glfw.KEY_I in self.touch and self.touch[glfw.KEY_I] > 0:
            self.cam.transformation.rotation_euler[pyrr.euler.index().roll] -= 0.1
        if glfw.KEY_K in self.touch and self.touch[glfw.KEY_K] > 0:
            self.cam.transformation.rotation_euler[pyrr.euler.index().roll] += 0.1
        if glfw.KEY_J in self.touch and self.touch[glfw.KEY_J] > 0:
            self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] -= 0.1
        if glfw.KEY_L in self.touch and self.touch[glfw.KEY_L] > 0:
            self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] += 0.1
        
        
        
        
        
        
"""
if glfw.KEY_UP in self.touch and self.touch[glfw.KEY_UP] > 0:
    self.objs[0].transformation.translation += \
        pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([0, 0, 0.02]))
if glfw.KEY_DOWN in self.touch and self.touch[glfw.KEY_DOWN] > 0:
    self.objs[0].transformation.translation -= \
        pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([0, 0, 0.02]))
if glfw.KEY_LEFT in self.touch and self.touch[glfw.KEY_LEFT] > 0:
    self.objs[0].transformation.rotation_euler[pyrr.euler.index().yaw] -= 0.1
if glfw.KEY_RIGHT in self.touch and self.touch[glfw.KEY_RIGHT] > 0:
    self.objs[0].transformation.rotation_euler[pyrr.euler.index().yaw] += 0.1

if glfw.KEY_I in self.touch and self.touch[glfw.KEY_I] > 0:
    self.cam.transformation.rotation_euler[pyrr.euler.index().roll] -= 0.1
if glfw.KEY_K in self.touch and self.touch[glfw.KEY_K] > 0:
    self.cam.transformation.rotation_euler[pyrr.euler.index().roll] += 0.1
if glfw.KEY_J in self.touch and self.touch[glfw.KEY_J] > 0:
    self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] -= 0.1
if glfw.KEY_L in self.touch and self.touch[glfw.KEY_L] > 0:
    self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] += 0.1


if glfw.KEY_SPACE in self.touch and self.touch[glfw.KEY_SPACE] > 0:
    self.cam.transformation.rotation_euler = self.objs[0].transformation.rotation_euler.copy() 
    self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] += np.pi
    self.cam.transformation.rotation_center = self.objs[0].transformation.translation + self.objs[0].transformation.rotation_center
    self.cam.transformation.translation = self.objs[0].transformation.translation + pyrr.Vector3([0, 1, 5])
"""
