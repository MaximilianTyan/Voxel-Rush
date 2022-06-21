from viewerGL import ViewerGL
import glutils
from mesh import Mesh
from cpe3d import Object3D, Camera, Transformation3D, Text
import numpy as np
#import OpenGL.GL as GL
import pyrr
from player import Player
from background import Background
from level import Level
from menus import Menus
import init



def main():
    change2D = input("Replace 'texture2D' with 'texture' in .frag files ?\n\
            On linux, replacing 'texture2D' with 'texture' should work\n\
            On Windows keeping 'texture2D' should work\n\
            \"Or at least it works on my machine\"\n\
            Proceed to replace ? y/n\n>")
    folder = 'frag_2D' if change2D == 'y' else 'frag_no2D'
    
    
    mainSwitch = ['title', 0]
    
    viewer = ViewerGL(mainSwitch)
    
    camera = Camera()
    viewer.set_camera(camera)
    viewer.cam.transformation.translation.z = 10
    #viewer.cam.transformation.rotation_center = viewer.cam.transformation.translation.copy()
    viewer.cam.transformation.rotation_center = pyrr.Vector3([0,0,0])

    program3d_id = glutils.create_program_from_file('shaders/vert/shader.vert',  f'shaders/{folder}/shader.frag')
    programGUI_id = glutils.create_program_from_file('shaders/vert/gui.vert',    f'shaders/{folder}/gui.frag')
    
    Object3D.set_program(program3d_id)
    Text.set_program(programGUI_id)
    
    init.init_classes() # initialises objects
    
    player = Player(mainSwitch)
    #player.hitboxvisible = True
    viewer.set_player(player)
    viewer.add_clocked_object(player)
    
    bkg = Background(camera)
    viewer.set_background(bkg.get_walls())
    
    level = Level(camera, showhitbox=False)
    viewer.set_terrain(level)
    viewer.add_clocked_object(level)
    
    viewer.add_object('level', level.get_obstacles())
    player.set_terrain(level)

    # for obj in viewer.objs:
    #     print(type(obj), obj.get_coords())
        
    #load_reference(viewer)
    for color in ('red','purple','yellow','green','blue'):
        Text.add_font(color, 'ressources/fonts/font_' + color + '.jpg')
    
    vao = Text.initalize_geometry()
    
    menus = Menus()
    viewer.set_menus(menus)
    #show_axis(viewer)
    
    viewer.run()



def show_axis(viewer):
    m = Mesh()
    p0, p1, p2, p3 = [0, 0, 0], [5, 0, 0], [0, 5, 0], [0, 0, 5]
    n = [0, 1, 0]
    c0, cx, cy, cz = [1, 1, 1], [1, 0, 0], [0, 1, 0], [0, 0, 1]
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]
    m.vertices = np.array([[p0 + n + c0 + t0], [p1 + n + cx + t1], [p2 + n + cy + t2], [p3 + n + cz + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3], [0, 1, 3]], np.uint32)
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles())
    o.wireframe = True
    viewer.add_object('common', o)

"""
    m = Mesh.load_obj('ressources/meshes/stegosaurus.obj')
    m.normalize()
    m.apply_matrix(pyrr.matrix44.create_from_scale([2, 2, 2, 1]))
    tr = Transformation3D()
    tr.translation.y = -np.amin(m.vertices, axis=0)[1]
    tr.translation.z = -5
    tr.rotation_center.z = 0.2
    texture = glutils.load_texture('ressources/textures/stegosaurus.jpg')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr)
    viewer.add_object(o)

    m = Mesh()
    p0, p1, p2, p3 = [-25, 0, -25], [25, 0, -25], [25, 0, 25], [-25, 0, 25]
    n, c = [0, 1, 0], [1, 1, 1]
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    texture = glutils.load_texture('ressources/textures/grass.jpg')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, Transformation3D())
    viewer.add_object(o)

    vao = Text.initalize_geometry()
    texture = glutils.load_texture('ressources/textures/fontB.jpg')
    o = Text('Bonjour les', np.array([-0.8, 0.3], np.float32), np.array([0.8, 0.8], np.float32), vao, 2, programGUI_id, texture)
    viewer.add_object(o)
    o = Text('3ETI', np.array([-0.5, -0.2], np.float32), np.array([0.5, 0.3], np.float32), vao, 2, programGUI_id, texture)
    viewer.add_object(o)
    """

if __name__ == '__main__':
    main()

