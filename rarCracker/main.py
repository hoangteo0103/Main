import gc
import logging
import os
import threading
from multiprocessing import Pipe
from queue import Queue

# import fastzipfile
from unrar import rarfile
from rarCracker.breakpoint import BreakPoint
from rarCracker.default_breakpoint import DefaultBreakPoint
from rarCracker.default_provider import DefaultProvider
from rarCracker.provider import Provider

from kivymd.icon_definitions import md_icons
class RarCracker:

    def __init__(self, file_path: str, start: int = 1, stop: int = 10, charset=None, output: str = './output',
                 workers: int = 4, level=logging.INFO, unrar_tool: str = 'unrar', provider: Provider = None,
                 break_point: BreakPoint = None):
        if os.path.exists(file_path):
            self.file_path = file_path
            self.output = output
            self.workers = workers
            self.file = None
            self.need_password = False
            try:
                self.file = rarfile.RarFile(self.file_path, 'r')
            except:
                self.need_password = True
            if provider is None:
                self.provider = DefaultProvider(start, stop, charset=charset)
            else:
                self.provider = provider
            if break_point is None:
                self.break_point = DefaultBreakPoint()
            else:
                self.break_point = break_point
            logging.basicConfig(level=level,
                                format='%(asctime)s - [Thread:%(thread)d] - %(levelname)s: %(message)s')
        else:
            raise FileNotFoundError(file_path)

    def crack(self, callback):
        if self.need_password:
            queue = Queue(maxsize=self.workers)
            lock = threading.Lock()
            sema = threading.Semaphore(value=self.workers)
            parent_pipe, child_pipe = Pipe()
            for i in self.break_point.generate(self.provider, self.file):
                if lock.locked():
                    return parent_pipe.recv()
                else:
                    sema.acquire()
                    queue.put(i)
                    thread = self.CrackThread(self.file_path, self.output, lock, i, sema, child_pipe, queue, callback)
                    thread.start()
            queue.join()
            if lock.locked():
                return parent_pipe.recv()
            else:
                return None
        else:
            logging.info('password empty')
            return ''

    class CrackThread(threading.Thread):
        def __init__(self, file, output, lock, password, sema, pipe, queue: Queue, callback):
            super().__init__()
            self.file = file
            self.output = output
            self.lock = lock
            self.password = password
            self.sema = sema
            self.pipe = pipe
            self.queue = queue
            self.callback = callback

        def run(self) -> None:
            # self.sema.acquire()
            if self.lock.locked():
                # logging.debug('password found')
                self.sema.release()
                gc.collect()
                self.queue.get()
                self.queue.task_done()
                return
            else:
                try:
                    with rarfile.RarFile(self.file, 'r', pwd=self.password) as rf:
                        rf.extractall(path='./output', pwd=self.password)
                    # logging.info('password {} is correct, password found'.format(self.password))
                    self.callback('password {} is correct, password found'.format(self.password))
                    self.lock.acquire()
                    self.sema.release()
                    self.pipe.send(self.password)
                    self.queue.get()
                    self.queue.task_done()
                    return
                except Exception as e:
                    self.callback('password {} is not correct'.format(self.password))
                    # logging.info('password {} is not correct'.format(self.password))
                    self.sema.release()
                    gc.collect()
                    self.queue.get()
                    self.queue.task_done()
                    return
