#!/usr/bin/env python
# coding=utf-8
"""
Rafael S. Guimaraes <rafaelg@ifes.edu.br>
http://rafaelguimaraes.net
"""
from threading import Thread
from multiprocessing import Queue
import sys
import select
import os

class Controller(object):
    """
     Class controller
    """
    def __init__(self):
        """
            Inicializator
            Queues for sender and receiver
        """
        self.sender_queue = Queue()
        self.receiver_queue = Queue()

    def start(self):
        """
            Run threads for incoming and outgoing messages;
        """
        self.sender = Thread(target=_sender, args=(self.message,self.sender_queue))
        self.sender.start()

        self.receiver = Thread(target=_receiver, args=(self.message,self.receiver_queue))
        self.receiver.start()


def _sender(message, queue):
    """ sender to router """
    while True:
        try:
            # Write commando to stdout
            line = sys.stdout
            line.write("%s\n" % message )
            line.flush()
        except:
            pass

def _receiver(message, queue):
    """ receiver from router """
    while True:
        try:
            # Can not use readline with select.
            # From http://stackoverflow.com/questions/5486717/python-select-doesnt-signal-all-input-from-pipe
            # Note that internally file.readlines([size]) loops and invokes the read() syscall more than once, attempting to fill an internal buffer of size. The first call to read() will immediately return, since select() indicated the fd was readable. However the 2nd call will block until data is available, which defeats the purpose of using select. In any case it is tricky to use file.readlines([size]) in an asynchronous app.
            response = os.read(sys.stdin.fileno(),4096)
            if not response:
                break
            message = response
            try:
                r,_,_ = select.select([sys.stdin], [], [], 1.0)
            except select.error:
                raise KeyboardInterrupt('Interrupt received in select')
        except:
            pass

if __name__ == "__main__":
    controller = Controller()




