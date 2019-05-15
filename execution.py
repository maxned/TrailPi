
import subprocess
import helpers
import time
import signal
import os

scripts = ["trailpi.py", "image_capture.py", "image_upload.py", "check_in.py"]

# Kill all scripts including self (useful for debugging)
def kill_everything(signum, frame):
    for script in scripts:
        pid = helpers.get_pid(script)
        if pid != 0:
            os.kill(pid, signal.SIGKILL)
    raise

signal.signal(signal.SIGINT, kill_everything)

# Make sure directory for crashlogs exists
if not "crashlogs" in os.listdir():
    os.mkdir("crashlogs")

# Launch all of the scripts and relaunch them if they crash
while True:
    for script in scripts:
        pid = helpers.get_pid(script)

        # Restart script if it crashed or hasn't been started yet
        if pid == 0:
            ps = subprocess.Popen("python3 {} 2>crashlogs/{}.crashlog &".format(script, script), shell=True)

    # Recheck for crashed scripts every so often
    time.sleep(60)
