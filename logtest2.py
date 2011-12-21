import logging

from logtest import MultiProcessingTest
from silence import Silence

def do_test():
    mp = MultiProcessingTest()
    mp.start()
    mp.stop()

if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

    print 'Normal:'
    do_test()
    print 'DONE'

    print '\nSilenced:'
    with Silence():
        do_test()
    print 'DONE'
