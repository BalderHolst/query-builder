class START:
    def __init__(self, history):
        self.history = history
        self.history.append('START')
    
    def SELECT(self, cols): return SELECT(self.history, cols)
    def __repr__(self): return ' '.join(self.history)
    
class SELECT:
    def __init__(self, history, cols):
        self.history = history
        self.history.append('SELECT')
        self.history.append(cols)
    
    def FROM(self, source): return FROM(self.history, source)
    def WHERE(self, expr): return WHERE(self.history, expr)
    def GROUP_BY(self, cols): return GROUP_BY(self.history, cols)
    def DISTINCT(self, cols): return DISTINCT(self.history, cols)
    def ALL(self, cols): return ALL(self.history, cols)
    def __repr__(self): return ' '.join(self.history)
    
class DISTINCT:
    def __init__(self, history, cols):
        self.history = history
        self.history.append('DISTINCT')
        self.history.append(cols)
    
    def FROM(self, source): return FROM(self.history, source)
    def WHERE(self, expr): return WHERE(self.history, expr)
    def GROUP_BY(self, cols): return GROUP_BY(self.history, cols)
    def __repr__(self): return ' '.join(self.history)
    
class ALL:
    def __init__(self, history, cols):
        self.history = history
        self.history.append('ALL')
        self.history.append(cols)
    
    def FROM(self, source): return FROM(self.history, source)
    def WHERE(self, expr): return WHERE(self.history, expr)
    def GROUP_BY(self, cols): return GROUP_BY(self.history, cols)
    def __repr__(self): return ' '.join(self.history)
    
class FROM:
    def __init__(self, history, source):
        self.history = history
        self.history.append('FROM')
        self.history.append(source)
    
    def END(self): return END(self.history, )
    def GROUP_BY(self, cols): return GROUP_BY(self.history, cols)
    def WHERE(self, expr): return WHERE(self.history, expr)
    def __repr__(self): return ' '.join(self.history)
    
class WHERE:
    def __init__(self, history, expr):
        self.history = history
        self.history.append('WHERE')
        self.history.append(expr)
    
    def GROUP_BY(self, cols): return GROUP_BY(self.history, cols)
    def END(self): return END(self.history, )
    def __repr__(self): return ' '.join(self.history)
    
class GROUP_BY:
    def __init__(self, history, cols):
        self.history = history
        self.history.append('GROUP_BY')
        self.history.append(cols)
    
    def HAVING(self, expr): return HAVING(self.history, expr)
    def __repr__(self): return ' '.join(self.history)
    
class HAVING:
    def __init__(self, history, expr):
        self.history = history
        self.history.append('HAVING')
        self.history.append(expr)
    
    def END(self): return END(self.history, )
    def __repr__(self): return ' '.join(self.history)
    