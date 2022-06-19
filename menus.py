from cpe3d import Text
import numpy as np

class Menus():
    def __init__(self):
        self.text_dict = {}
        self.load_gui()
    
    def get_text(self, switch):
        mode, lvl = switch[0], switch[1]
        if mode == 'level':
            return self.text_dict[mode]
        
        if mode == 'select':
            difficulty = ('green', 'yellow', 'red','purple')
            color = difficulty[lvl % len(difficulty)]
            self.text_dict[mode][-1].set_font(color)
        
        return self.text_dict['common'] + self.text_dict[mode]
    
    def add_text(self, key, text):
        if key not in self.text_dict.keys():
            self.text_dict[key] = [text]
        else:
            self.text_dict[key].append(text)
    
    def load_gui(self):
        voxel_label = Text('Voxel', np.array([-0.3, 0.4], np.float32), np.array([0.2, 0.8], np.float32))
        voxel_label.set_font('yellow')
        self.add_text('common', voxel_label)
        
        rush_label = Text('RUSH', np.array([-0.3, 0.1], np.float32), np.array([0.3, 0.5], np.float32))
        rush_label.set_font('blue')
        self.add_text('common', rush_label)

        press_label = Text('Press SPACE to start', np.array([-0.8, -0.5], np.float32), np.array([0.8, -0.4], np.float32))
        press_label.set_font('red')
        self.add_text('title', press_label)
        
        level_label = Text('Level &', np.array([-0.3, -0.6], np.float32), np.array([0.3, -0.2], np.float32))
        level_label.set_font('green')
        self.add_text('select', level_label)
        
        pause_label = Text('Press Space to resume, Escape to quit', np.array([-0.8, -0.5], np.float32), np.array([0.8, -0.4], np.float32))
        pause_label.set_font('red')
        self.add_text('pause', pause_label)
        
        score_label = Text('try &', np.array([-0.9, 0.7], np.float32), np.array([-0.5, 0.9], np.float32))
        score_label.set_font('yellow')
        self.add_text('level', score_label)
        
        

