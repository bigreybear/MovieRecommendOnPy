import numpy as np

def insider_watcher(obj):
    for row in dir(obj):
        print row
    print 'And Type is {}'.format(type(obj))


if __name__ == '__main__':
    b = np.zeros((100, 100))
    print b