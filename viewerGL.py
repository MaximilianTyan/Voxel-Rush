#!/usr/bin/env python3

import OpenGL.GL as GL
import glfw
import pyrr
import numpy as np
import time
import ctypes

from cpe3d import Object3D

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
        print(f"[SETUP] OpenGL: {GL.glGetString(GL.GL_VERSION).decode('ascii')}")

        self.prevtime = 0
        self.background = []
        self.clocked_objs= []
        self.objs = {}
        self.touch = {}
        self.slow_time = False
        self.show_all_hitboxes = False
        

    def run(self):

        # # Camera follow player
        # player_pos = self.player.transformation.translation.xyz
        # cam_offset = pyrr.Vector3([3, 3, 10])
        # cam_center = [1,0,1] * player_pos + cam_offset
        # self.cam.transformation.translation = cam_center
        # self.cam.transformation.rotation_center = cam_center
        print('-'*10 + "Objects" + '-'*10)
        print('[RUN] camera:', self.cam)
        print('[RUN] background:', self.background)
        print('[RUN] terrain:', self.terrain)
        print('[RUN] menus:', self.menus)
        print('[RUN] sounds:', self.musicmanager)
        print('[RUN] objs:', self.objs)
        print('[RUN] clocked:', self.clocked_objs)
        
        self.musicmanager.load_music('robtop-geometry-dash-menu-theme.mp3')
        self.musicmanager.music.play(loop=True)
        self.musicmanager.load_sound('victory', 'ff-vii-victory-theme.mp3')
        
        # boucle d'affichage
        while not glfw.window_should_close(self.window):
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

            #print(self.switch)
            
            self.update_key()
            
            #print(self.player.transformation.translation.x)
            if self.switch[0] == 'level':
                crt_time = glfw.get_time()
                dt = crt_time - self.prevtime
                self.prevtime = crt_time
                
                if self.slow_time:
                    dt *= 0.1
                
                for obj in self.clocked_objs:
                    obj.tick_clock(dt, crt_time)
                
                if self.player.transformation.translation.x >= self.terrain.finish_line:
                    self.switch[0] = 'select'
                    self.player.reset()
                    self.musicmanager.music.stop()
                    self.musicmanager.sounds['victory'].play(block=True)
                
                deaths = self.player.deathcount
                self.menus.text_dict['level'][-1].format([deaths])
                
            elif self.switch[0] == 'select':
                filename = self.terrain.get_files_list()[self.switch[1]]
                self.menus.text_dict['select'][-1].format([self.terrain.get_lvl_name(filename)])
            
            # Camera follow player
            player_pos = self.player.transformation.translation.xyz
            
            cam_offset = pyrr.Vector3([3, 0, 10])
            if self.switch[0] not in ('level', 'pause'):
                cam_offset.x = self.player.transformation.offset.x
                
            if player_pos.y < 6:
                cam_offset.y = 3
                cam_center = [1,0,1] * player_pos + cam_offset
            else:
                cam_offset.y = -3
                cam_center = player_pos + cam_offset
            
            self.cam.transformation.translation = cam_center
            self.cam.transformation.rotation_center = cam_center
            
            # Background follows camera
            for wall in self.background:
                wall.transformation.translation.x = self.cam.transformation.translation.x
            
            #print('cam pos:\t', self.cam.transformation.translation.xyz)
            #print('player pos:\t', self.player.transformation.translation.xyz)
            #print('wall pos:\t', self.background[0].transformation.translation.xyz)
            
            #print('### LIST OBJS:', self.background, self.objs[self.switch[0]], self.objs['common'])
            #print('### LIST OBJS:',self.background, self.player, self.objs.get(self.switch[0], []), self.menus.get_text(self.switch))
            with_hitbox = [self.player] + self.objs.get(self.switch[0], []) 
            obj_list = self.background + with_hitbox + self.menus.get_text(self.switch)
            #print(obj_list)
            for i, obj in enumerate(obj_list):
                if obj.visible:
                    if obj.program is None: 
                        raise Exception(f"Le programme de rendu n'a pas été précisé : {obj.program} at {obj}")
                    GL.glUseProgram(obj.program)
                    #print(obj, obj.program)

                    if isinstance(obj, Object3D):
                        self.update_camera(obj.program)
                    obj.draw()

                    if obj.hitboxvisible or self.show_all_hitboxes:
                        if obj in with_hitbox:
                            #print('draw hitbox', obj)
                            obj.hitbox.transformation.translation = obj.transformation.translation
                            obj.hitbox.draw()

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
    
    def set_terrain(self, terrain):
        self.terrain = terrain
    
    def set_menus(self, menus):
        self.menus = menus
    
    def set_player(self, player):
        self.player = player

    def set_sound(self, sound):
        self.musicmanager = sound

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
                self.player.jump()
            if glfw.KEY_S in self.touch and self.touch[glfw.KEY_S] > 0:
                self.slow_time = True
            else:
                self.slow_time = False
            
            if glfw.KEY_R in self.touch and self.touch[glfw.KEY_R] > 0:
                self.player.death()
                
            if glfw.KEY_ESCAPE in self.touch and self.touch[glfw.KEY_ESCAPE] > 0:
                del self.touch[glfw.KEY_ESCAPE]
                self.switch[0] = 'pause'
                self.musicmanager.music.pause()
                
        elif self.switch[0] == 'pause':
            if glfw.KEY_ESCAPE in self.touch and self.touch[glfw.KEY_ESCAPE] > 0:
                del self.touch[glfw.KEY_ESCAPE]
                self.switch[0] = 'select'
                self.player.reset()
                self.musicmanager.load_music('robtop-geometry-dash-menu-theme.mp3')
                self.musicmanager.music.play(loop=True)
                
            if glfw.KEY_SPACE in self.touch and self.touch[glfw.KEY_SPACE] > 0:
                del self.touch[glfw.KEY_SPACE]
                self.switch[0] = 'level'
                self.musicmanager.music.resume()
        
        elif self.switch[0] == 'title':
            if glfw.KEY_ESCAPE in self.touch and self.touch[glfw.KEY_ESCAPE] > 0:
                glfw.set_window_should_close(self.window, glfw.TRUE)
            if glfw.KEY_SPACE in self.touch and self.touch[glfw.KEY_SPACE] > 0:
                del self.touch[glfw.KEY_SPACE]
                self.switch[0] = 'select'
                self.switch[1] = 0
                self.player.reset()

        elif self.switch[0] == 'select':
            if glfw.KEY_ESCAPE in self.touch and self.touch[glfw.KEY_ESCAPE] > 0:
                del self.touch[glfw.KEY_ESCAPE]
                self.switch[0] = 'title'
                
            if glfw.KEY_RIGHT in self.touch and self.touch[glfw.KEY_RIGHT] > 0:
                del self.touch[glfw.KEY_RIGHT]
                self.switch[1] = min(self.switch[1]+1, len(self.terrain.get_files_list())-1)
            
            if glfw.KEY_LEFT in self.touch and self.touch[glfw.KEY_LEFT] > 0:
                del self.touch[glfw.KEY_LEFT]
                self.switch[1] = max(self.switch[1]-1, 0)
                
            
            if glfw.KEY_SPACE in self.touch and self.touch[glfw.KEY_SPACE] > 0:
                del self.touch[glfw.KEY_SPACE]                
                self.terrain.set_level(self.terrain.get_files_list()[self.switch[1]])
                self.terrain.load()
                self.objs['level'] = self.terrain.get_obstacles()
                print('='*10 + f'Started level {self.switch[1]}' + '='*10)
                
                self.player.reset()
                self.player.step_start()

                self.switch[0] = 'level'
                glfw.set_time(0)
                self.prevtime = 0
                self.musicmanager.music.play()

                
        if glfw.KEY_H in self.touch and self.touch[glfw.KEY_H] > 0:
            del self.touch[glfw.KEY_H]                
            self.show_all_hitboxes = not self.show_all_hitboxes
            self.player.wireframe = self.show_all_hitboxes
            print('[KEY] show_all_hitboxes changed to', self.show_all_hitboxes)
            

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
            self.cam.transformation.translation.z += 0.02
        if glfw.KEY_DOWN in self.touch and self.touch[glfw.KEY_DOWN] > 0:
            self.cam.transformation.translation.z -= 0.02
        if glfw.KEY_LEFT in self.touch and self.touch[glfw.KEY_LEFT] > 0:
            self.cam.transformation.translation.x -= 0.02
        if glfw.KEY_RIGHT in self.touch and self.touch[glfw.KEY_RIGHT] > 0:
            self.cam.transformation.translation.x += 0.02
        """
        
        
        
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
