#coding:utf-8

from obstacles import Spike, Cube

class LevelError(Exception):
    def __init__(self, *args) -> None:
        super().__init__(*args)

class Level():
    def __init__(self, level=0):
        self.file = f"levels/level_{level}.txt"
    
    def load(self):
        with open(self.file) as file:
            map = file.readlines()

        for y,row in enumerate(map):
            x = row.find('S')
            if x != -1:
                self.start_pos = (x, y)
                break
        if x == -1: raise LevelError('Level file does not contain a starting position')

        print(self.start_pos)

        for i, row in map:
            for j, element in row:

                if element == '.':
                    continue
                elif element == '@':
                    continue
                elif element == '^':
                    continue
                elif element == 'v':
                    continue

    def add_element():
        pass


class Terrain():
    def __init__(self, level=0):
        pass




