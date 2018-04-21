import subprocess
import re
import winsound
from queue import Queue
from threading import Thread
import time
import pyperclip
import sys



def ping (ip, mode = 'default'):
    process = subprocess.Popen(['ping','-n','1','-w','5000',ip],stdout=subprocess.PIPE)
    out,err=process.communicate()
    reply_string = out.decode('utf-8')

    if mode == 'default':
        return ip
    elif mode == 'STATUS':
        i = 0
        while not (('Reply from ' + ip) in reply_string):
            process = subprocess.Popen(['ping', '-n', '1', '-w', '5000', ip], stdout=subprocess.PIPE)
            out, err = process.communicate()
            reply_string = out.decode('utf-8')
            i = i + 1
            if i == 3:
                break
        else:
            return True
        return False
    elif mode == 'SHOW_REPLY':
        print(reply_string)


def subnet_scanner(network):
    r = re.search(r"\d*\.\d*\.\d*\.", network)
    ip = r.group()
    ipList = []
    ipUpList = []
    for i in range(1,255):
        ipList.append(ip + str(i))

    def do_stuff(q):
      while True:
        ip = q.get()
        if ping(ip,'STATUS'):
            ipUpList.append(ip)
        q.task_done()

    q = Queue(maxsize=0)
    num_threads = 200

    for i in range(num_threads):
      worker = Thread(target=do_stuff, args=(q,))
      worker.setDaemon(True)
      worker.start()

    for ip in ipList:
      q.put(ip)

    q.join()
    s = '['
    ipUpList.sort()
    for ip in ipUpList:
        print(ip)
        s = s + '\'' + ip + '\','
    s = s + ']'
    pyperclip.copy(s)

start = time.time()
subnet_scanner(sys.argv[1])
# print(ping('10.80.0.2','STATUS'))
print(time.time()-start)
