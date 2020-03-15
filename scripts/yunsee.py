from lib.config import *
from lib.requests_url import post_req

def yunsee_info(simple_url):
    query_url = "http://www.yunsee.cn/home/getInfo"
    data = {"type": "webinfo", "url": simple_url}

    print(current_time("yellow").format("yunsee指纹查询中..."))
    print(current_time("sep_prefix"))

    result = post_req(query_url, data=data).json()
    if int(result["code"]) == 1:
        print(current_time("green").format("server：" + result["res"]["server"]))
        print(current_time("green").format("status：" + str(result["res"]["status_code"])))
        print(current_time("green").format("language：" + result["res"]["language"]))

        for k, v in result["res"]["fingers"].items():
            print(current_time("green").format(str(k) + "：" + str(v)))
            
        print(current_time("green").format("title：" + result["res"]["title"]))
        print(current_time("green").format("email：" + result["res"]["whois_mail"]))
        print(current_time("green").format("waf：" + result["res"]["waf"]))
        print(current_time("green").format("ip：" + result["res"]["ip"]))
        print(current_time("green").format("cms：" + result["res"]["cms"]))
        print(current_time("green").format("cdn：" + result["res"]["cdn"]))
        print(current_time("green").format("idc：" + result["res"]["idc"]))
    else:
        print(current_time("red").format("查询频率过快，请稍后在查..."))
    print(current_time("sep_suffix"))