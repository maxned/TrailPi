
import subprocess
import os
import signal
import time

def get_pid(name):
    # Get the PID of the process with the name given
    cmd = "ps -aef | grep '%s' | grep -v 'grep' | awk '{ print $2 }'"
    ps = subprocess.Popen(cmd % name, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    # Communicate returns a tuple of the standard output and standard error
    output = ps.communicate()[0]
    if output:
        return int(output)
    else:
        return 0

pid = get_pid("image_capture")
print(pid)

time.sleep(2)
os.kill(pid, signal.SIGUSR2)
time.sleep(10)
os.kill(pid, signal.SIGUSR1)
