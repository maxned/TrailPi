
import subprocess
import helpers
import time

processes = ["trailpi.py", "image_capture.py", "image_upload.py", "check_in.py"]

while True:
    for process in processes:
        pid = helpers.get_pid(process)

        # Restart process if it crashed or hasn't been started yet
        if pid == 0:
            ps = subprocess.Popen("python3 %s&" % process, shell=True)

    # Recheck for crashed processes every so often
    time.sleep(60)
