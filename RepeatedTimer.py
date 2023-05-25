import threading
import time
import sys
sys.path.append('/usr/local/lib/python3.8/dist-packages')
sys.path.append('/usr/lib/python3/dist-packages')
#####                             Repeated timer by sec                      #######
class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.next_call = time.time()
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self.next_call += self.interval
            self._timer = threading.Timer(self.next_call - time.time(), self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

#RepeatedTimer(secs,function,params)
#rt = RepeatedTimer(1, sys.argv[2], param)