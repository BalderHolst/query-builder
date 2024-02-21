
class START:
    def __init__(self):
        pass
    def SELECT(self, cols): pass


class SELECT:
    def __init__(self, cols):
        self.cols = cols
    def FROM(self, source): pass
    def WHERE(self, expr): pass
    def GROUP_BY(self, cols): pass
    def DISTINCT(self, cols): pass
    def ALL(self, cols): pass


class DISTINCT:
    def __init__(self, cols):
        self.cols = cols
    def FROM(self, source): pass
    def WHERE(self, expr): pass
    def GROUP_BY(self, cols): pass


class ALL:
    def __init__(self, cols):
        self.cols = cols
    def FROM(self, source): pass
    def WHERE(self, expr): pass
    def GROUP_BY(self, cols): pass


class FROM:
    def __init__(self, source):
        self.source = source
    def END(self): pass
    def GROUP_BY(self, cols): pass
    def WHERE(self, expr): pass


class WHERE:
    def __init__(self, expr):
        self.expr = expr
    def GROUP_BY(self, cols): pass
    def END(self): pass


class GROUP_BY:
    def __init__(self, cols):
        self.cols = cols
    def HAVING(self, expr): pass


class HAVING:
    def __init__(self, expr):
        self.expr = expr
    def END(self): pass


class END:
    def __init__(self):
        pass
