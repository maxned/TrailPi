
import subprocess

# From the Python Cookbook
# Default list is populated with tuples of (None, None) as specified
# by empty_object
class RingBuffer:
    def __init__(self, size_max, empty_object=(None, None)):
        self.max = size_max
        self.default_object = empty_object
        self.current = 0
        self.clear()

    # Append an element overwriting the oldest one
    def append(self, x):
        self.data[self.current] = x
        self.current = (self.current + 1) % self.max

    # Return elements from oldest to newest
    def get(self):
        return self.data[self.current:] + self.data[:self.current]

    def clear(self):
        self.data = [self.default_object for i in range(self.max)]

# Return the PID of a process specified by name
def get_pid(name):
    # Get the PID of the process with the name given
    cmd = "ps -aef | grep '%s' | grep -v 'grep' | awk '{ print $2 }'"
    ps = subprocess.Popen(cmd % name, shell=True, stdout=subprocess.PIPE)

    # Communicate returns a tuple of the standard output and standard error
    output = ps.communicate()[0]
    if output:
        return int(output)
    else:
        return 0
