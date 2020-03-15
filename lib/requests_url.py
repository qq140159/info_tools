from urllib.parse import urlparse
from lib.config import *
import requests
import sys
import re

def get_req(query_url, cookies="", timeout=10):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        'Referer': "https://www.baidu.com",
        'Connection': 'Keep-Alive',
    }
    try:
        result = requests.get(url=query_url, headers=headers, verify=True, timeout=timeout, cookies=cookies)
        if result.text or str(result.status_code)[0] == "2" or str(result.status_code)[0] == "3" or str(result.status_code)[0] == "4":
            return result
        return None
    except requests.exceptions.ConnectTimeout:
        print(current_time("red").format(("{}  --  连接超时...").format(query_url)))
    except requests.exceptions.ReadTimeout:
        print(current_time("red").format(("{}  --  读取超时...").format(query_url)))
    except requests.exceptions.ConnectionError:
        print(current_time("red").format(("{}  --  连接异常...").format(query_url)))
    except BaseException as e:
        print("error", e)


def post_req(query_url, data="", cookies="", timeout=10):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        'Referer': "https://www.baidu.com",
        'Connection': 'Keep-Alive',
    }
    try:
        result = requests.post(url=query_url, headers=headers, data=data, verify=True, timeout=timeout, cookies=cookies)
        if result.text or str(result.status_code)[0] == "2" or str(result.status_code)[0] == "3" or str(result.status_code)[0] == "4":
            return result
        return None
    except requests.exceptions.ConnectTimeout:
        print(current_time("red").format(("{}  --  连接超时...").format(query_url)))
    except requests.exceptions.ReadTimeout:
        print(current_time("red").format(("{}  --  读取超时...").format(query_url)))
    except requests.exceptions.ConnectionError:
        print(current_time("red").format(("{}  --  连接异常...").format(query_url)))
    except BaseException as e:
        print("error", e)

def url_parse(url):
    parse_list = urlparse(url.strip())
    agree = parse_list.scheme
    if agree:
        if agree in "https":
            simple_url = parse_list.netloc
            if ":" in simple_url:
                simple_url = simple_url.split(":")[0]
            complete_url = (agree + "://" + parse_list.netloc + parse_list.path).strip("/")
            return simple_url, complete_url
    else:
        print(current_time("red").format("url请带上http或https!!!"))
        sys.exit(0)

def get_encode(result):
    pattern = re.compile("<meta.*?charset=(.*?)>", re.S)
    try:
        encod = re.sub("[\",\/,\',<,>]", "", re.findall(pattern, result.text)[0])
        return encod
    except:
        return "utf-8"

def get_title(result_text):
    title_pattern = re.compile("<title>(.*?)</title>", re.S)
    try:
        title = re.findall(title_pattern, result_text)[0]
        return title
    except:
        return "None"












