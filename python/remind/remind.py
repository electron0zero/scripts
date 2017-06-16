import time
from threading import Thread  # This is the right package name
from win10toast import ToastNotifier


class UpdateThread(Thread):

    def __init__(self):
        self.stopped = False
        Thread.__init__(self)  # Call the super constructor (Thread's one)

    def run(self):
        while not self.stopped:
            self.showMeToast()
            # time.sleep(1)
            time.sleep(1800)  # every 30 mins

    def showMeToast(self):
        toaster = ToastNotifier()
        toaster.show_toast("Get Back to Work", "Just Checking, do not procrastinate, work on shit")

# create the repeating thing
myThread = UpdateThread()
# Start the thing
myThread.start()
