from viewerGL import ViewerGL
import glutils
from mesh import Mesh
from cpe3d import Object3D, Camera, Transformation3D, Text
import numpy as np
import OpenGL.GL as GL
import pyrr
from player import Player
from background import Background
from level import Level

def main():
    viewer = ViewerGL()
    
    camera = Camera()
    viewer.set_camera(camera)
    viewer.cam.transformation.translation.z = 10
    #viewer.cam.transformation.rotation_center = viewer.cam.transformation.translation.copy()

    program3d_id = glutils.create_program_from_file('shaders/shader.vert', 'shaders/shader.frag')
    programGUI_id = glutils.create_program_from_file('shaders/gui.vert', 'shaders/gui.frag')
    
    Object3D.set_program(program3d_id)
    Text.set_program(programGUI_id)
    
    player = Player()
    viewer.add_ref_object('player', player)
    viewer.add_clocked_object(player)
    
    bkg = Background()
    viewer.add_object(bkg.get_walls())

    level = Level(camera, level="test")
    viewer.add_clocked_object(player)
    level.load()
    viewer.add_object(level.get_objects())
    
    from obstacles import Spike
    viewer.add_object(Spike(0,0,0))

    # for obj in viewer.objs:
    #     print(type(obj), obj.get_coords())
        
    #load_reference(viewer)
    viewer.run()



def load_reference(viewer):
    m = Mesh()
    p0, p1, p2, p3 = [0, 0, 0], [5, 0, 0], [0, 5, 0], [0, 0, 5]
    n = [0, 1, 0]
    c0, cx, cy, cz = [1, 1, 1], [1, 0, 0], [0, 1, 0], [0, 0, 1]
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]
    m.vertices = np.array([[p0 + n + c0 + t0], [p1 + n + cx + t1], [p2 + n + cy + t2], [p3 + n + cz + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3], [0, 1, 3]], np.uint32)
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles())
    o.wireframe = True
    viewer.add_object(o)

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

