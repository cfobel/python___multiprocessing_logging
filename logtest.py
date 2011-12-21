from time import sleep
from datetime import datetime
import logging

import multiprocessing


class TestChild(object):
    def __init__(self, conn):
        self.conn = conn
        
    def main(self):
        self.conn.send('ready')

        while True:
            if self.conn.poll():
                command = self.conn.recv()
                if command == 'stop':
                    logging.info('stop')
                    break
                elif command == 'start':
                    logging.info('start')
            #sleep(1. / 100)
        self.conn.send('done')
        return


class MultiProcessingTest(object):
    def __init__(self):
        self.conn, self.child_conn = multiprocessing.Pipe()
        self.child = self._launch_child()

    def _pipe_pull(self):
        while True:
            if self.conn.poll():
                return self.conn.recv()
            sleep(1. / 100)
    
    def _launch_child(self):
        p = multiprocessing.Process(target=self._start_child)
        p.start()
        while True:
            response = self._pipe_pull()
            if response == 'ready':
                break
            else:
                raise Exception('Invalid response from child')
        logging.info('child is ready')
        return p

    def _start_child(self):
        child = TestChild(self.child_conn)
        child.main()

    def start(self):
        logging.info('request start: %s' % datetime.now())
        self.conn.send('start')

    def stop(self):
        logging.info('request stop: %s' % datetime.now())
        self.conn.send('stop')
        if self.child:
            response = self._pipe_pull()
            self.child.join()
        else:
            response = None
        del self.child
        return response


def do_test():
    logging.info('Testing testing, 1, 2, 3')

if __name__ == '__main__':
    do_test()
