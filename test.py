from out import *

q = START([]).SELECT('a').FROM('b').WHERE('c').GROUP_BY('d')

print(q)
