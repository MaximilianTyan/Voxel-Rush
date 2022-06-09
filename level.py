#coding:utf-8
import math
from obstacles import Spike, Cube, Jump

class LevelError(Exception):
    def __init__(self, *args) -> None:
        super().__init__(*args)

class Level():
    def __init__(self, camera, level=0):
        self.file = f"levels/level_{level}.txt"
        self.camera = camera
        self.obstacles = []
        
    def add_element(self, element):
        element.visible = True
        self.obstacles.append(element)
    
    def get_relevant_aabb(self, px, py):
        relevant_aabb = []
        for obj in self.obstacles:
            if px -1.5 <= obj.transformation.translation.x <= px + 1 and \
                py -1.5 <= obj.transformation.translation.y <= py + 1:
                relevant_aabb.append(obj)
        return relevant_aabb

    def load(self):
        with open(self.file) as file:
            map = file.readlines()

        self.start_pos = None
        self.finish_line = None
        finishx = None
        for y,row in enumerate(map):
            
            # Starting position detection
            startx = row.find('S')
            if startx != -1:
                if self.start_pos != None:
                    raise LevelError('Level contains more than one starting position')
                self.start_pos = (startx, len(map) - y)
            
            # Finish line detection
            finishx = row.find('|')
            if finishx != -1:
                if (self.finish_line != None) and (self.finish_line[0] != finishx):
                    raise LevelError('Finish line should be a vertical line')
                self.finish_line = (finishx, len(map) - y)
        
        if startx == -1: raise LevelError('Level file does not contain a starting position')
        if finishx == -1: raise LevelError('Level file does not contain a finish line')

        print("Starting position:", self.start_pos)
        print("Finish line:", self.finish_line)
        
        for i, row in enumerate(map):
            for j, element in enumerate(row.strip()):
                x = j - self.start_pos[0]
                y = len(map) - i - self.start_pos[1]
                
                if element in ('.', 'S', '|'):
                    continue
                elif element == '@':
                    obj = Cube(x, y, 0)
                elif element == '^':
                    obj = Spike(x, y, 0, 'UP')
                elif element == 'v':
                    obj = Spike(x, y, 0, 'DOWN')
                elif element == '<':
                    obj = Spike(x, y, 0, 'LEFT')
                elif element == 'J':
                    obj = Jump(x,y, 0)
                else:
                    raise LevelError(f"Unsupported element:'{element}'")
                #print(x,y, element, j, i)
                self.add_element(obj)

    def tick_clock(self, dt, crttime):
        cx, cy, cz = self.camera.transformation.translation.xyz
        
        test_offset = 0
        
        FOV_width = abs((cz - test_offset) * math.tan((180/math.pi)*self.camera.fovx)/2 )
        FOV_height = abs((cz - test_offset) * math.tan((180/math.pi)*self.camera.fovy)/2)
        
        FOV_UpLeft = (cx - FOV_width / 2, cy + FOV_height / 2)
        
        #print((cx, cy, cz), self.camera.fovx, self.camera.fovy)
        #print(FOV_width, FOV_height)
        #print(FOV_UpLeft, (FOV_UpLeft[0] + FOV_width, FOV_UpLeft[1] - FOV_height))
        
        for element in self.obstacles:
            
            if (FOV_UpLeft[0] <= element.transformation.translation.x <= FOV_UpLeft[0] + FOV_width) \
                and (FOV_UpLeft[1] >= element.transformation.translation.y >= FOV_UpLeft[1] - FOV_height):
                    element.visible = True
            else:
                element.visible = False
            #print(element.transformation.translation.xyz, element.visible)
        
    


