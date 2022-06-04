#coding:utf-8
import math
from obstacles import Spike, Cube

class LevelError(Exception):
    def __init__(self, *args) -> None:
        super().__init__(*args)

class Level():
    def __init__(self, camera, level=0):
        self.file = f"levels/level_{level}.txt"
        self.terrain = Terrain()
        self.camera = camera
    
    def get_objects(self):
        return self.terrain.obstacles

    def load(self):
        with open(self.file) as file:
            map = file.readlines()

        for y,row in enumerate(map):
            x = row.find('S')
            if x != -1:
                self.start_pos = (x, len(map) - y)
                break
        if x == -1: raise LevelError('Level file does not contain a starting position')

        print("Starting position:", self.start_pos)

        for i, row in enumerate(map):
            for j, element in enumerate(row.strip()):
                x = j - self.start_pos[0]
                y = i - self.start_pos[1]
                
                if element in ('.', 'S'):
                    continue
                elif element == '@':
                    obj = Cube(x, y, 0)
                elif element == '^':
                    obj = Spike(x, y, 0, 'UP')
                elif element == 'v':
                    obj = Spike(x, y, 0, 'DOWN')
                elif element == '<':
                    obj = Spike(x, y, 0, 'LEFT')
                else:
                    raise LevelError(f"Unsupported element:'{element}'")
                print(x,y, element, j, i)
                self.terrain.add_element(obj)

    def update_render(self):
        cx, cy, cz = self.camera.transformation.translation.xyz
        
        FOV_width = cz * math.tan(self.camera.fovx)
        FOV_height = cz * math.tan(self.camera.fovy)
        
        FOV_UpLeft = (cx - FOV_width / 2, cy + FOV_height / 2)
        
        for element in self.terrain.obstacles:
            if (FOV_UpLeft[0] <= element.translation.x <= FOV_UpLeft[0] + FOV_width) \
                and (FOV_UpLeft[1] <= element.transformation.translation.y <= FOV_UpLeft[1] + FOV_height):
                    element.visible = True
            else:
                element.visible = False
    
class Terrain():
    def __init__(self):
        self.obstacles = []
    
    def add_element(self, element):
        element.visible = True
        self.obstacles.append(element)

    def collision_test(self, x, y):
        pass



