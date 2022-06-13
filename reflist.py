#coding:utf-8

class reflist(list):
    """
    List subclass integrating key value pair assignment to
    ease readibility access to elements    
    """

    def __init__(self):
        super().__init__(self)
        self._refdict = {}
    
    def __getitem__(self, index):
        if not isinstance(index, int) and index in self._refdict.keys():
            return self[self._refdict[index]]
        else:
            return list.__getitem__(self, index)
    
    def __repr__(self):
        return list.__repr__(self) + ' ' + dict.__repr__(self._refdict)
    
    def refappend(self, key, value):
        self._refdict[key] = len(self)
        self.append(value)
    
    def link(self, key, index:int):
        if index < 0:
            index = len(self) + index
        self._refdict[key] = index

if __name__ == '__main__':
    test = reflist()
    test.refappend('test', None)
    test.append(52)
    test.append(print)
    test.link('func', -1)
    test += [1, True]
    print(test)
    print(test[1])
    print(test['test'])
