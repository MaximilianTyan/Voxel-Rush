import OpenGL.GL as GL
import pyrr
import numpy as np 

class Transformation3D: 
    def __init__(self, euler = pyrr.euler.create(), center = pyrr.Vector3(), translation = pyrr.Vector3(), offset = pyrr.Vector3()):
        self.rotation_euler = euler.copy()
        self.rotation_center = center.copy()
        self.translation = translation.copy()
        self.offset = offset.copy()

class Object:
    def __init__(self, vao, nb_triangle, program, texture):
        self.vao = vao
        self.nb_triangle = nb_triangle
        self.program = program
        self.texture = texture
        self.visible = True
        self.wireframe = False
        self.hitboxvisible = False
    
    def __repr__(self):
        return str(type(self))[8:-2]

    def draw(self):
        if self.visible:
            if type(self).program is None: 
                raise Exception("Le programme de rendu n'a pas été précisé")
            GL.glUseProgram(type(self).program)
            GL.glBindVertexArray(self.vao)
            if self.texture is not None:
                GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture)
            if self.wireframe:
                draw_type = GL.GL_LINE_LOOP
            else:
                draw_type = GL.GL_TRIANGLES
            GL.glDrawElements(draw_type, 3*self.nb_triangle, GL.GL_UNSIGNED_INT, None)

class Object3D(Object):
    def __init__(self, vao, nb_triangle, texture=None, transformation=Transformation3D()):
        super().__init__(vao, nb_triangle, type(self).program, texture)
        self.transformation = transformation
    
    @classmethod
    def set_program(cls, program):
        cls.program = program
    
    def get_aabb_points(self):
        minpt, maxpt = self.bounding_box
        minpt = minpt + self.transformation.translation
        maxpt = maxpt + self.transformation.translation
        
        delta = maxpt - minpt

        pmin1 = minpt + delta * [1, 0, 0]
        pmin2 = minpt + delta * [0, 1, 0]
        pmin3 = minpt + delta * [0, 0, 1]
        
        pmax1 = maxpt - delta * [1, 0, 0]
        pmax2 = maxpt - delta * [0, 1, 0]
        pmax3 = maxpt - delta * [0, 0, 1]

        return minpt,  pmin1, pmin2, pmin3, pmax1, pmax2, pmax3, maxpt
    
    def get_aabb_faces_center(self):
        minpt, maxpt = self.bounding_box
        delta = maxpt - minpt
        center = self.get_coords() + self.transformation.offset
        
        half_dx = delta * [1, 0, 0] / 2
        negx = center - half_dx
        posx = center + half_dx
        
        half_dy = delta * [0, 1, 0] / 2
        negy = center - half_dy
        posy = center + half_dy
        
        half_dz = delta * [0, 0, 1] / 2
        negz = center - half_dz
        posz = center + half_dz

        return negx, posx, negy, posy, negz, posz
        
    def get_coords(self):
        return self.transformation.translation.xyz

    
    def draw(self):
        
        if not self.visible:
            return
        
        if Object3D.program is None: 
            raise Exception("Le programme de rendu n'a pas été précisé")
        GL.glUseProgram(Object3D.program)

        # Récupère l'identifiant de la variable pour le programme courant
        loc = GL.glGetUniformLocation(self.program, "translation_model")
        # Vérifie que la variable existe
        if (loc == -1) :
            print("Pas de variable uniforme : translation_model")
        # Modifie la variable pour le programme courant
        translation = self.transformation.translation
        GL.glUniform4f(loc, translation.x, translation.y, translation.z, 0)
        
        # Récupère l'identifiant de la variable pour le programme courant
        loc = GL.glGetUniformLocation(self.program, "offset_model")
        # Vérifie que la variable existe
        if (loc == -1) :
            print("Pas de variable uniforme : offset_model")
        # Modifie la variable pour le programme courant
        offset = self.transformation.offset
        GL.glUniform4f(loc, offset.x, offset.y, offset.z, 0)

        # Récupère l'identifiant de la variable pour le programme courant
        loc = GL.glGetUniformLocation(self.program, "rotation_center_model")
        # Vérifie que la variable existe
        if (loc == -1) :
            print("Pas de variable uniforme : rotation_center_model")
        # Modifie la variable pour le programme courant
        rotation_center = self.transformation.rotation_center
        GL.glUniform4f(loc, rotation_center.x, rotation_center.y, rotation_center.z, 0)

        rot = pyrr.matrix44.create_from_eulers(self.transformation.rotation_euler)
        loc = GL.glGetUniformLocation(self.program, "rotation_model")
        if (loc == -1) :
            print("Pas de variable uniforme : rotation_model")
        GL.glUniformMatrix4fv(loc, 1, GL.GL_FALSE, rot)

        super().draw()

class Camera:
    def __init__(self, transformation = Transformation3D(translation=pyrr.Vector3([0, 1, 0], dtype='float32')), projection=None):
        self.transformation = transformation
        if projection is None:
            self.ratio = 1.778  #(width / height)
            self.fovy = 60  #degrees
            self.fovx = self.fovy * self.ratio
            self.projection = pyrr.matrix44.create_perspective_projection(self.fovy, self.ratio, 0.01, 100)

class Text(Object):
    def __init__(self, value, bottomLeft, topRight, vao, nb_triangle, texture):
        self.value = value
        self.bottomLeft = bottomLeft
        self.topRight = topRight
        super().__init__(vao, nb_triangle, type(self).program, texture)

    @classmethod
    def set_program(cls, program):
        cls.program = program

    def draw(self):
        if Text.program is None: 
            raise Exception("Le programme de rendu n'a pas été précisé")
        GL.glUseProgram(Text.program)
        GL.glDisable(GL.GL_DEPTH_TEST)
        size = self.topRight-self.bottomLeft
        size[0] /= len(self.value)
        loc = GL.glGetUniformLocation(self.program, "size")
        if (loc == -1) :
            print("Pas de variable uniforme : size")
        GL.glUniform2f(loc, size[0], size[1])
        GL.glBindVertexArray(self.vao)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture)
        for idx, c in enumerate(self.value):
            loc = GL.glGetUniformLocation(self.program, "start")
            if (loc == -1) :
                print("Pas de variable uniforme : start")
            GL.glUniform2f(loc, self.bottomLeft[0]+idx*size[0], self.bottomLeft[1])

            loc = GL.glGetUniformLocation(self.program, "c")
            if (loc == -1) :
                print("Pas de variable uniforme : c")
            GL.glUniform1i(loc, np.array(ord(c), np.int32))

            GL.glDrawElements(GL.GL_TRIANGLES, 3*2, GL.GL_UNSIGNED_INT, None)
        GL.glEnable(GL.GL_DEPTH_TEST)

    @staticmethod
    def initalize_geometry():
        p0, p1, p2, p3 = [0, 0, 0], [0, 1, 0], [1, 1, 0], [1, 0, 0]
        geometrie = np.array([p0+p1+p2+p3], np.float32)
        index = np.array([[0, 1, 2]+[0, 2, 3]], np.uint32)
        vao = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(vao)
        vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, geometrie, GL.GL_STATIC_DRAW)
        GL.glEnableVertexAttribArray(0)
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 0, None)
        vboi = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER,vboi)
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER,index,GL.GL_STATIC_DRAW)
        return vao

