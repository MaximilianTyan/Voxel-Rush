#coding:utf-8

from audioplayer import AudioPlayer

class AudioManager():
    
    def __init__(self):
        print('[SETUP] Audio manager initialized')
        self.sounds = {}
        self.music = None
        
    def load_sound(self, name, filename):
        if name in self.sounds.keys():
            self.sounds[name].close()
        print('[SOUNDS] Loading music .\\ressources\\sounds\\' + str(filename) + "as " + str(name))
            
        self.sounds[name] = AudioPlayer(".\\ressources\\sounds\\" + str(filename))
        self.sounds[name].volume = 100
        print(self.sounds)
    
    def restart_music(self):
        self.music.stop()
        self.music.play()
    
    def load_music(self, filename):
        if isinstance(self.music, AudioPlayer):
            #print(self.music.filename)
            self.music.close()
            #print(self.music.filename)
        
        if filename == 'None':
            print('[SOUNDS] No music to load, stopping current music')
            return
        
        print('[SOUNDS] Loading music .\\ressources\\musics\\' + str(filename))
        
        self.music = AudioPlayer(".\\ressources\\musics\\" + str(filename))
        #print(self.music.filename)
        self.music.volume = 75
