#coding:utf-8
import math
import obstacles

class LevelError(Exception):
    def __init__(self, *args) -> None:
        super().__init__(*args)

class Level():
    def __init__(self, camera, level=0):
        self.file = f"levels/level_{level}.txt"
        self.camera = camera
        self.obs = []
        
    def add_element(self, element):
        element.visible = True
        self.obs.append(element)
    
    def get_near_obstacles(self, px, py):
        obs = []
        for obj in self.obs:
            if px -1.5 <= obj.transformation.translation.x <= px + 1 and \
                py -1.5 <= obj.transformation.translation.y <= py + 1:
                obs.append(obj)
        return obs

    def get_obstacles(self):
        return self.obs
    
    def load(self):
        print("Loading level {}...".format(self.file))
        with open(self.file) as file:
            map = file.readlines()

        self.start_pos = None
        self.finish_line = None
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
                if (self.finish_line != finishx) and (self.finish_line != None):
                    raise LevelError('Finish line should be a vertical line')
                self.finish_line = finishx
        
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
                    obj = obstacles.Cube(x, y, 0)
                elif element == '^':
                    obj = obstacles.Spike(x, y, 0, 'UP')
                elif element == 'v':
                    obj = obstacles.Spike(x, y, 0, 'DOWN')
                elif element == '<':
                    obj = obstacles.Spike(x, y, 0, 'LEFT')
                elif element == 'J':
                    obj = obstacles.Jump(x,y, 0)
                else:
                    raise LevelError(f"Unsupported element:'{element}'")
                #print(x,y, element, j, i)
                self.add_element(obj)

    def tick_clock(self, dt, crttime):
        cx, cy, cz = self.camera.transformation.translation.xyz
        
        test_offset = -1
        
        FOV_width = abs((cz - test_offset) * math.tan((180/math.pi)*self.camera.fovx)/2 )
        FOV_height = abs((cz - test_offset) * math.tan((180/math.pi)*self.camera.fovy)/2)
        
        FOV_UpLeft = (cx - FOV_width / 2, cy + FOV_height / 2)
        
        #print((cx, cy, cz), self.camera.fovx, self.camera.fovy)
        #print(FOV_width, FOV_height)
        #print(FOV_UpLeft, (FOV_UpLeft[0] + FOV_width, FOV_UpLeft[1] - FOV_height))
        
        for element in self.obs:
            
            if (FOV_UpLeft[0] <= element.transformation.translation.x <= FOV_UpLeft[0] + FOV_width) \
                and (FOV_UpLeft[1] >= element.transformation.translation.y >= FOV_UpLeft[1] - FOV_height):
                    element.visible = True
            else:
                element.visible = False
            #print(element.transformation.translation.xyz, element.visible)
        
    


