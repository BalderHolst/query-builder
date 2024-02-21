
class START:
    def __init__(self):
        pass
    def SELECT(self, cols): return SELECT(cols)


class SELECT:
    def __init__(self, cols):
        self.cols = cols
    def FROM(self, source): return FROM(source)
    def WHERE(self, expr): return WHERE(expr)
    def GROUP_BY(self, cols): return GROUP_BY(cols)
    def DISTINCT(self): return DISTINCT()
    def ALL(self): return ALL()


class DISTINCT:
    def __init__(self):
        pass
    def FROM(self, source): return FROM(source)
    def WHERE(self, expr): return WHERE(expr)
    def GROUP_BY(self, cols): return GROUP_BY(cols)


class ALL:
    def __init__(self):
        pass
    def FROM(self, source): return FROM(source)
    def WHERE(self, expr): return WHERE(expr)
    def GROUP_BY(self, cols): return GROUP_BY(cols)


class FROM:
    def __init__(self, source):
        self.source = source
    def END(self): return END()
    def GROUP_BY(self, cols): return GROUP_BY(cols)
    def WHERE(self, expr): return WHERE(expr)


class WHERE:
    def __init__(self, expr):
        self.expr = expr
    def GROUP_BY(self, cols): return GROUP_BY(cols)
    def END(self): return END()


class GROUP_BY:
    def __init__(self, cols):
        self.cols = cols
    def HAVING(self, expr): return HAVING(expr)


class HAVING:
    def __init__(self, expr):
        self.expr = expr
    def END(self): return END()


class END:
    def __init__(self):
        pass

SELECT("test").ALL().FROM("table").END
