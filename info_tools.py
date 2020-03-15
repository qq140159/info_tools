import os
import re
import sys
from colorama import init
init(autoreset=True)
from gevent import monkey
monkey.patch_all()
from lib.config import current_time
from lib.cmdline import parse_args
from lib.requests_url import url_parse
from lib.write_html_file import Write_Html
from scripts.aizhan_whois import aizhan_whois
from scripts.ipc_record import ipc_record
from scripts.yunsee import yunsee_info
from scripts.dir_scan import run_dir_sacn
from scripts.nmap_scan import run_nmap
from scripts.get_domains.main import domain_main

def match_file_result(tmp_result_file, result_file):
    try:
        file = tmp_result_file
        with open(file, "r+", encoding="utf-8") as f:
            result_list = f.readlines()
            f.seek(0)
            f.truncate()
        with open(result_file, "a+", encoding="utf-8") as f:
            for row in result_list:
                pattern = re.compile("\[.*?\](.*)\[", re.S)
                result = re.findall(pattern, row)
                if result:
                    for i in result:
                        i = str(i.strip(""))
                        if "爱站whois" in i or "备案查询中" in i or "指纹查询中" in i or "nmap扫描中" in i or "目录扫描" in i or "开始域名" in i:
                            f.write("\r\n" + i + "\n")
                        else:
                            f.write(i + "\n")

        if (os.path.exists(tmp_result_file)):
            os.remove(tmp_result_file)
    except:
        print(current_time("red").format("文件操作失败..."))

class Logger(object):
    def __init__(self, filename="Default.log"):
        self.terminal = sys.stdout
        self.filename = filename
    def write(self, message):
        with open(self.filename, "a", encoding="utf-8") as f:
            self.terminal.write(message)
            f.write(message)
    def flush(self):
        pass

def start(url, args):
    simple_url, complete_url = url_parse(url)
    tmp_result_file = "./report/" + "tmp_" + simple_url + ".txt"
    tmp_port = "./report/" + "tmp_" + simple_url + "_port" + ".txt"
    result_file = "./report/" + simple_url + ".txt"
    html_file = "./report/" + simple_url + ".html"

    sys.stdout = Logger(tmp_result_file)
    if args.all:
        aizhan_whois(simple_url)
        ipc_record(simple_url)
        yunsee_info(simple_url)
        run_nmap(args.thread, simple_url, tmp_port)
        if not args.dir:
            args.dir = "./dict/js.txt"
        run_dir_sacn(args.thread, complete_url, args.dir)
        domain_main(simple_url)
    else:
        if args.whois:
            aizhan_whois(simple_url)
        if args.ipc:
            ipc_record(simple_url)
        if args.yunsee:
            yunsee_info(simple_url)
        if args.nmap:
            run_nmap(args.thread, simple_url, tmp_port)
        if args.dir:
            run_dir_sacn(args.thread, complete_url, args.dir)
        if args.sub_domain:
            domain_main(simple_url)
    match_file_result(tmp_result_file, result_file)
    Write_Html(result_file, html_file).write()

if __name__ == '__main__':
    args = parse_args()
    type = sys.getfilesystemencoding()
    
    url_file = args.Url_file
    if url_file:
        with open(url_file, "r", encoding="utf-8") as f:
            url_list = f.readlines()
            for url in url_list:
                url = url.strip()
                start(url, args)
    else:
        url = args.url
        start(url, args)
    


