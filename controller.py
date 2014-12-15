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
        :rtype : object
        """
        self.sender_queue = Queue()
        self.receiver_queue = Queue()
        self.message_sent = []
        self.message_received = []

    def start(self):
        """
            Run threads for incoming and outgoing messages;
        """
        self.sender = Thread(target=_sender, args=(self.message_sent, self.sender_queue))
        self.sender.start()

        self.receiver = Thread(target=_receiver, args=(self.message_received, self.receiver_queue))
        self.receiver.start()


def _sender(message, queue):
    """ sender to router """
    while len(message) > 0:
        try:
            # Write commando to STDOUT
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
def timed (message="", **preample):
    import time
    now = time.strftime('%a, %d %b %Y %H:%M:%S',time.localtime())
    return "%s | %-8s | %-6d | %-13s | %s" % (now,'FORKED',os.getpid(), preample['name'], message)

if __name__ == "__main__":
    import datetime
    import exabgp.version
    preample = { "name": "SDNRouter",
                 "date": datetime.datetime.now(),
                 "version": "0.1",
                 "exabgp_version": exabgp.version.version
    }
    sys.stderr.write(timed("-"*60+"\n", **preample))
    sys.stderr.write(timed("Starting Controller...\n", **preample))
    sys.stderr.write(timed("Starting integration with ExaBGP version %(exabgp_version)s\n" % (preample), **preample))
    sys.stderr.write(timed("-"*60+"\n", **preample))
    controller = Controller()
    controller.start()