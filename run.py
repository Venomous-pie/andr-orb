import subprocess
import sys
import os
import signal
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

process = None

def start():
    global process
    process = subprocess.Popen(
        [sys.executable, "main.py"],
        preexec_fn=os.setsid  
    )

def restart():
    global process
    if process:
        os.killpg(os.getpgid(process.pid), signal.SIGKILL)  # force kill
        process.wait()
    time.sleep(0.5)  # brief pause before restart
    start()

class Handler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(".py") and "run.py" not in event.src_path:
            print(f"\n🔄 {event.src_path} changed, restarting...")
            restart()

start()

observer = Observer()
observer.schedule(Handler(), path=".", recursive=False)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
    if process:
        os.killpg(os.getpgid(process.pid), signal.SIGKILL)

observer.join()