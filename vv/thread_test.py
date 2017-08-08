import time
import random
import threading

class RunningThread(threading.Thread):
    def __init__(self, identificador, timeout):
        threading.Thread.__init__(self)
        self.id = identificador
        self.timeout = timeout

    def run(self):
        print(self.timeout)
        time.sleep(self.timeout)
        pool.release()
        print('THREAD FIM {0} => {1}'.format(self.id, self.timeout))

class Handler(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        jobs = []
        for i in range(10):
            pool.acquire()
            job = RunningThread(i, int(random.random() * 10))
            job.setDaemon(True)
            job.start()
            jobs.append(job)
        for job in jobs:
            job.join()
        print('HANDLER THREAD FIM')
        

thread_count = 10
pool = threading.BoundedSemaphore(value = thread_count)
handler = Handler()
handler.start()
handler.join()
print('MAIN THREAD FIM')