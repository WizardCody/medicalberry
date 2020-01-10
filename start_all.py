import os
import sys
import atexit
import time
import subprocess


processes = []
processes.append(subprocess.Popen(['python3', 'homeguard/base/temp.py'], stderr=sys.stderr, stdout=sys.stdout))
processes.append(subprocess.Popen(['python3', 'homeguard/base/mq-7.py'], stderr=sys.stderr, stdout=sys.stdout))

processes.append(subprocess.Popen(['python3', 'MiBand2/start.py'], stderr=sys.stderr, stdout=sys.stdout))


def kill_children():
    for process in processes:
        process.kill()
    

atexit.register(kill_children)

while True:
    time.sleep(1.0)
    pass

sys.exit()