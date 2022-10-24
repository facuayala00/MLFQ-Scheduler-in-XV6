from subprocess import Popen, PIPE
import time

p = Popen(["make", "CPUS=1", "qemu"], stdout=PIPE, stdin=PIPE)
time.sleep(1)

p.stdin.write("iobench &; iobench\n".encode())
p.stdin.close()

for line in iter(p.stdout.readline, ""):
    if not line:
        break
    print(line.decode().rstrip())
