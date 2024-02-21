
class START:
    def __init__(self, history=[]):
        self.history = history + ['START']
    def SELECT(self, cols): return SELECT(cols, history=self.history)
    def __repr__(self): return ' '.join(self.history)


class SELECT:
    def __init__(self, cols, history=[]):
        self.history = history + ['SELECT']
        self.cols = cols
    def FROM(self, source): return FROM(source, history=self.history)
    def WHERE(self, expr): return WHERE(expr, history=self.history)
    def GROUP_BY(self, cols): return GROUP_BY(cols, history=self.history)
    @property
    def DISTINCT(self): return DISTINCT(history=self.history)
    @property
    def ALL(self): return ALL(history=self.history)
    def __repr__(self): return ' '.join(self.history)


class DISTINCT:
    def __init__(self, history=[]):
        self.history = history + ['DISTINCT']
    def FROM(self, source): return FROM(source, history=self.history)
    def WHERE(self, expr): return WHERE(expr, history=self.history)
    def GROUP_BY(self, cols): return GROUP_BY(cols, history=self.history)
    def __repr__(self): return ' '.join(self.history)


class ALL:
    def __init__(self, history=[]):
        self.history = history + ['ALL']
    def FROM(self, source): return FROM(source, history=self.history)
    def WHERE(self, expr): return WHERE(expr, history=self.history)
    def GROUP_BY(self, cols): return GROUP_BY(cols, history=self.history)
    def __repr__(self): return ' '.join(self.history)


class FROM:
    def __init__(self, source, history=[]):
        self.history = history + ['FROM']
        self.source = source
    def END(self): return END(history=self.history)
    def GROUP_BY(self, cols): return GROUP_BY(cols, history=self.history)
    def WHERE(self, expr): return WHERE(expr, history=self.history)
    def __repr__(self): return ' '.join(self.history)


class WHERE:
    def __init__(self, expr, history=[]):
        self.history = history + ['WHERE']
        self.expr = expr
    def GROUP_BY(self, cols): return GROUP_BY(cols, history=self.history)
    def END(self): return END(history=self.history)
    def __repr__(self): return ' '.join(self.history)


class GROUP_BY:
    def __init__(self, cols, history=[]):
        self.history = history + ['GROUP BY']
        self.cols = cols
    def HAVING(self, expr): return HAVING(expr, history=self.history)
    def __repr__(self): return ' '.join(self.history)


class HAVING:
    def __init__(self, expr, history=[]):
        self.history = history + ['HAVING']
        self.expr = expr
    def END(self): return END(history=self.history)
    def __repr__(self): return ' '.join(self.history)


class END:
    def __init__(self, history=[]):
        self.history = history + ['END']
    def __repr__(self): return ' '.join(self.history)

q = SELECT("*").DISTINCT.FROM("TaBLe").WHERE("a = 4")
