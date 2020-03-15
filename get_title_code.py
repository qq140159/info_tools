import gevent
from gevent import monkey
monkey.patch_all()
from gevent.queue import Queue
from colorama import init
init(autoreset=True)
from lib.requests_url import get_req, get_title, get_encode
import socket
import re
import os

url_list = []
ip_list = []
queue = Queue()

def get_ip(red_file, wri_file):
    ip_lst = []
    with open(red_file, 'r+') as f:
        ip_pattern = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', re.S)
        for ip in f.readlines():
            ip = re.findall(ip_pattern, ip)
            for i in ip:
                i = "http://" + str(i)
                if i not in ip_lst:
                    ip_lst.append(i)

    for i in ip_lst:
        write_file(content=i, wri_file=wri_file)

def match_url(url):
    url_list = re.findall("\w{0,100}\.\w{0,100}\.?\w{0,100}\.?\w{0,100}\.?\w{0,100}\.?\w{0,100}\.?\w{0,100}", url, re.S)
    if len(url_list) == 0:
        pass
    elif len(url_list) == 1:
        if url_list[0][0] != ".":
            return url_list[0]
    else:
        for u in url_list:
            split_list = u.split(".")
            if len(split_list) == 4:
                for i in split_list[0]:
                    if i not in [str(ii) for ii in range(11)]:
                        return url_list[0]
            else:
                return url_list[0]

def read_url_file(url_file):
    with open(url_file, "r", encoding="utf-8") as f:
        for i in f.readlines():
            url = match_url(i.strip())
            url1 = "http://" + str(url)
            url2 = "https://" + str(url)
            if url1 and url1 not in url_list:
                url_list.append(url1)
                queue.put(url1)
                queue.put(url2)

def get_url_ip(url_list, file="defalt.txt"):
    for url in url_list:
        try:
            if "https://" not in url:
                url = re.sub("http(s)?://", "", url)
                addr = socket.gethostbyname(url)
                write_file(content=addr, wri_file=file, url=url)
        except:
            pass

def get_url_result(html_file):
    while True:
        if queue.empty():
            break
        else:
            url = queue.get()
            ip_list.append(url)
            result = get_req(url)
            if result == None:
                continue
            response_code = result.status_code
            result_encode = get_encode(result)
            result.encoding = result_encode
            response_title = get_title(result.text)
            write_file("""<a href="{}">{}</a>&emsp;&emsp;{}&emsp;&emsp;{}<br>""".format(url, url, response_code, response_title),html_file)

def write_file(content, wri_file, url=""):
    with open(wri_file, "a+", encoding="utf-8") as f:
        if url:
            f.write(url + " " * 6 + content + "\n")
        else:
            f.write(content + "\n")

def run(thread, html_file):
    thread_list = [gevent.spawn(get_url_result, html_file) for _ in range(thread)]
    gevent.joinall(thread_list)

if __name__ == '__main__':
    url_path = input("please input urlfile addr：")
    read_url_file(url_path)
    filename = input("please input save filename：")
    html_file = os.path.join(os.path.dirname(url_path),filename + ".html")
    url_ip_txt = os.path.join(os.path.dirname(url_path) ,filename + "_url_ip" + ".txt")
    ip_txt = os.path.join(os.path.dirname(url_path), filename + "_ip" + ".txt")
    thread = 100
    run(thread, html_file)
    get_url_ip(url_list, url_ip_txt)
    get_ip(url_ip_txt, ip_txt)
    print("已保存到：{}".format(html_file))
    print("已保存到：{}".format(url_ip_txt))
    print("已保存到：{}".format(ip_txt))







