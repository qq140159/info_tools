import gevent
from gevent import monkey
from gevent.queue import Queue
from lib.requests_url import get_encode,get_title
monkey.patch_all()
import requests
from lib.config import *
import datetime
import time
import signal

def run_dir_sacn(*params):
    signal.signal(signal.SIGINT, signal_quit)
    dir_scan_thread(*params)

def signal_quit(sig, frame):  #退出信号
    exit(-1)

def dir_scan_thread(thread, complete_url, dir_path):
    pass_list, lens  = Get_dir_list(dir_path, complete_url).get_pass_list()
    st = datetime.datetime.now()
    print(current_time("yellow").format("开始目录扫描..."))
    print(current_time("sep_prefix"))
    start = Dir_Scan(pass_list, complete_url, thread, lens)
    start.run()
    print(current_time("yellow").format("目录扫描耗时:" + str((datetime.datetime.now() - st).total_seconds()) + "秒"))
    print(current_time("sep_suffix"))

class Get_dir_list(object):
    def __init__(self, pass_path, url):
        self.pass_path = pass_path
        self.url = url

    def get_pass_list(self):
        try:
            with open(self.pass_path, "r+") as f:
                pass_list = []
                pass_lists = f.readlines()
                lens = len(pass_lists)
                for pwd in pass_lists:
                    pass_list.append("".join(pwd.split()))
            return pass_list, lens
        except:
            print("get_dir")

class Dir_Scan(object):
    def __init__(self, pass_list, url, thread, lens):
        self.pass_list = pass_list
        self.url = url
        self.thread = thread
        self.lens = lens
        self.q = Queue()
        self.count = 0

    def conntion_url(self, ref):
        global redirect_list, response_code
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
            'Referer': ref,
            'Connection': 'Keep-Alive',
        }
        while True:
            try:
                if self.q.empty():
                    break
                url = self.q.get_nowait()
                result = requests.get(url=url, headers=headers, allow_redirects=False, verify=True, timeout=5)
                self.count += 1
                result_code = result.status_code
                result_encode = get_encode(result)
                result.encoding = result_encode

                if result_code == 400 or str(result_code)[0] == "5" or result_code == 404 or result_code == 405:
                    continue

                elif result_code == 403:
                    print("\r" + current_time("yellow").format(url + "   " + str(result_code)))

                elif str(result_code)[0] == "3":
                    result = requests.get(url=url, headers=headers, verify=True, timeout=5)
                    if result.url in redirect_list or url == result.url:
                        continue

                    result_encode = get_encode(result)
                    result.encoding = result_encode

                    redirect_list.append(result.url)
                    print("\r" + current_time("blue").format(url + "   " + str(result_code) + "   " + "==========>" + "   " + result.url + "   " + "title: " + get_title(result.text)))
                    continue

                elif str(result_code)[0] == "2": 
                    if len(result.text) in response_code:
                        continue
                    if not response_code[0] > 0:
                        response_code.append(len(result.text))
                        response_code[0] += 1
                    print("\r" + current_time("green").format(url + "   " + str(result_code) + "   " + "title: " + get_title(result.text)))
                    continue

            except requests.exceptions.ConnectTimeout:
                #print(current_time("red").format(url + "    " + "连接超时..."))
                pass
            except requests.exceptions.ReadTimeout:
                #print(current_time("red").format(url + "    " + "读取超时..."))
                pass
            except requests.exceptions.ConnectionError:
                pass
                #print(current_time("red").format(url + "    " + "连接异常..."))
            except BaseException as e:
                pass
                #print(current_time("red").format("error：" + "    " + str(e)))
            except:
                print("未知错误")
                break

    def get_path(self):
        for i in self.pass_list:
            if i and i.strip()[0] == "/":
                self.q.put(self.url + str(i) + "/")
            else:
                self.q.put(self.url + "/" + str(i) + "/")
        ref = self.url
        return ref

    def run(self):
        count = 4
        st = datetime.datetime.now()
        try:
            ref = self.get_path()
            thread_lst = [gevent.spawn(self.conntion_url, ref) for i in range(self.thread)]
            while thread_lst:
                for t in thread_lst:
                    if t.dead:
                        thread_lst.remove(t)
                time.sleep(0.3)
                print('\r\033[1;32;40m{}线程数:{} 成功{}|总数{} 耗时:{}\033[1m'.format(char_set[count % 4], len(thread_lst), self.count, len(self.pass_list), str((datetime.datetime.now() - st).total_seconds())), end='')
                count += 1
            print("\r")
        except:
            for t in thread_lst:
                t.kill()
            print(current_time("red").format(current_time("red").format(str(1) + "协程启动失败...")))
            print(current_time("sep_suffix"))

