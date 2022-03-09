import codecs
import logging
import time
from multiprocessing import Pipe, Process, Queue

logging.basicConfig(filename='artifacts/hard_logs.txt',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)


def thread_a(q, ch):
    while True:
        time.sleep(5)
        ch.send(q.get().lower())


def thread_b(in_ch, out_ch):
    while True:
        out_ch.send(codecs.encode(in_ch.recv(), "rot_13"))


if __name__ == "__main__":
    ab_recv, ab_send = Pipe()
    mb_recv, mb_send = Pipe()
    q = Queue()
    a = Process(target=thread_a, args=[q, ab_send])
    a.start()
    b = Process(target=thread_b, args=[ab_recv, mb_send])
    b.start()
    while True:
        msg = input("> ")
        if msg == 'exit':
            logger.info(f'Exit')
            a.kill()
            b.kill()
            exit(0)
        logger.info(f'Receive "{msg}"')
        q.put(msg)
        cyphered = mb_recv.recv()
        logger.info(f'Receive cyphered"{cyphered}"')
        print(cyphered)
