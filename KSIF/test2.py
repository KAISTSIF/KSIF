"""

"""
import pickle, inspect

def foo(fox):
    print(fox)
    return 'what the fox say'+fox

f = open('foo.txt', 'wb')
pickle.dump(foo, f)
f.close()

g = open('foo.txt', 'rb')
hoo = pickle.load(g)
g.close()

for i in inspect.getsourcelines(hoo)[0]:
    print(i)

__author__ = 'Seung Hyeon Yu'
__email__ = 'rambor12@business.kaist.ac.kr'