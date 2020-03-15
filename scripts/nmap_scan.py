import threading
from lib.config import *
import traceback
import datetime
import signal
import time
import os

def run_nmap(*params):
    signal.signal(signal.SIGINT, signal_quit)
    nmap_scan_thread(*params)

def signal_quit(sig, frame):  #退出信号
    exit(-1)

def nmap_scan_thread(thread, simple_url, tmp_port):
    thread_lst = []
    pass_list = [i for i in range(1, 65535)]
    lens = len(pass_list)
    st = datetime.datetime.now()
    print(current_time("yellow").format("nmap扫描中{}...".format(simple_url)))
    print(current_time("sep_prefix"))
    count = 4
    try:
        for i in range(thread):
            fenpei = lens // thread
            mythd = Nmap_Scan((i * (fenpei))+1, (i + 1) * (fenpei), simple_url, tmp_port)
            if lens % thread > 0 and i == thread - 1:
                mythd = Nmap_Scan((i * (fenpei)) + 1, ((i + 1) * (fenpei)) + (lens % thread) + 1, simple_url, tmp_port)
            mythd.start()
            thread_lst.append(mythd)

        while thread_lst:
            for t in thread_lst:
                if not t.is_alive():
                    thread_lst.remove(t)
            time.sleep(0.3)
            print('\033[1;32;40m\r{}线程数：{} 耗时：{}\033[1m'.format(char_set[count % 4], len(thread_lst), str((datetime.datetime.now() - st).total_seconds())), end='')
            count += 1
        print("\r")

        mythd.match_file_port()
        sp = (datetime.datetime.now() - st).total_seconds()
        print(current_time("yellow").format("nmap扫描耗时:" + str(sp) + "秒"))
        print(current_time("sep_suffix"))
    except BaseException as e:
        print(current_time("red").format(current_time("red").format(str(e) + "线程启动失败...")))
        print(current_time("sep_suffix"))
        traceback.print_exc()

class Nmap_Scan(threading.Thread):
    def __init__(self, starts, ends, url, tmp_port_file):
        threading.Thread.__init__(self)
        self.lock = threading.Lock()
        self.starts = starts
        self.ends = ends
        self.url = url
        self.tmp_port_file = tmp_port_file

    def wirte_result(self, port_str):
        with self.lock:
            with open(self.tmp_port_file, "a+", encoding="utf-8") as f:
                f.write(str(port_str))

    def match_file_port(self):
        tmp_list = []
        with open(self.tmp_port_file, "r+", encoding="utf-8") as f:
            result_list = f.readlines()
            f.seek(0)
            f.truncate()
            for i in result_list:
                if "open" in i:
                    tmp_list.append(i.strip())

        if len(tmp_list) > 200:
            print(current_time("red").format("开放端口超过200个，应该被防火墙发现可，不显示..."))
        else:
            with open(self.tmp_port_file, "r+", encoding="utf-8") as f:
                f.write(self.url + "\n")
                for port in tmp_list:
                    f.write(port + "\n")
                    print(current_time("green").format(port))

        if (os.path.exists(self.tmp_port_file)):
            os.remove(self.tmp_port_file)

    def run(self):
        try:
            cmd = "nmap -sV -Pn -p{}-{} {} --open".format(self.starts, self.ends, self.url)
            result = os.popen(cmd, "r")
            self.wirte_result(result.read())
        except:
            print(current_time("red").format("线程{}nmap扫描失败").format(threading.current_thread().name))
            traceback.print_exc()