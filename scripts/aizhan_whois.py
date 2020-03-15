from lib.config import *
from lib.requests_url import get_req
import re

def aizhan_whois(simple_url):
    query_url = "https://whois.aizhan.com/{}".format(simple_url) + "/"
    print(current_time("yellow").format("爱站whois查询中..."))
    print(current_time("sep_prefix"))
    result = get_req(query_url)
    if result:
        try:
            result_text = result.text
            domain = re.findall("""<td class="thead">域名</td>.*?<td>(.*?)<""", result_text, re.S)[0]
            if domain.strip()[0] == "\'":
                print(current_time("red").format("url有误，请重试：" + query_url))
                print(current_time("sep_suffix"))
                return
        except:
            print(current_time("red").format("url有误，请重试：" + query_url))
            return

        registrar = re.findall("""<td class="thead">注册商</td>.*?<td>(.*?)<""", result_text, re.S)[0]
        domain_name = re.findall("""<td class="thead">域名持有人/机构名称</td>.*?<td>(.*?)<""", result_text, re.S)[0]
        create_time = re.findall("""<td class="thead">创建时间</td>.*?<span>(.*?)<""", result_text, re.S)[0]
        re_time = re.findall("""<td class="thead">更新时间</td>.*?<td>.*?<span>(.*?)<""", result_text, re.S)[0]
        expiration_date = re.findall("""<td class="thead">过期时间</td>.*?<span>(.*?)<""", result_text, re.S)[0]
        domain_server = re.findall("""<td class="thead">域名服务器</td>.*?<td>(\w.*?)<""", result_text, re.S)
        dns_server = re.findall("""<td class="thead">DNS服务器</td>.*?<td>(\w.*?)<""", result_text, re.S)
        try:
            email = re.findall("Tech Email.*?>(.*?)<", result_text, re.S)[0]
        except:
            email = []
        try:
            Tech_City = re.findall("Tech City.*?>(.*?)<", result_text, re.S)[0]
        except:
            Tech_City = []
        try:
            Tech_Street = re.findall("Tech Street.*?>(.*?)<", result_text, re.S)[0]
        except:
            Tech_Street = []
        if domain.strip() and domain.strip() != "-":
            print(current_time("green").format("域名：" + domain))
        if registrar.strip() and registrar.strip() != "-":
            print(current_time("green").format("注册商：" + registrar))
        if domain_name.strip() and domain_name.strip() != "-":
            print(current_time("green").format("域名持有人/机构名称：" + domain_name))
        if create_time.strip() and create_time.strip() != "-":
            print(current_time("green").format("创建时间：" + create_time))
        if re_time.strip() and re_time.strip() != "-":
            print(current_time("green").format("更新时间：" + re_time))
        if expiration_date.strip() and expiration_date.strip() != "-":
            print(current_time("green").format("过期时间：" + expiration_date))
        if domain_server:
            print(current_time("green").format("域名服务器：" + str(domain_server)))
        if dns_server:
            print(current_time("green").format("dns服务器：" + str(dns_server)))
        if email:
            print(current_time("green").format("注册人邮箱：" + str(email)))
        if Tech_City:
            print(current_time("green").format("城市：" + str(Tech_City)))
        if Tech_Street:
            print(current_time("green").format("街道：" + str(Tech_Street)))
    else:
        print(current_time("red").format("  请求错误..."))
    print(current_time("sep_suffix"))