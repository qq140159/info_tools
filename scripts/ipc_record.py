from lib.config import *
from lib.requests_url import get_req
import re

def ipc_record(simple_url):
    ipc_url = "https://icp.aizhan.com/" + simple_url
    print(current_time("yellow").format("站长工具备案查询中..."))
    print(current_time("sep_prefix"))

    result = get_req(ipc_url)
    if result:
        result_text = result.text
        url_error = re.findall("未找到", result_text, re.S)
        unit_name = re.findall("主办单位名称.*?<td>(.*?)</td>", result_text, re.S)
        unit_nature = re.findall("主办单位性质.*?<td>(.*?)</td>", result_text, re.S)
        website_filing = re.findall("网站备案/许可证号.*?<span>(.*?)</span>", result_text, re.S)
        website_name = re.findall("网站名称.*?<td>(.*?)</td>", result_text, re.S)
        Website_owner = re.findall("网站负责人.*?<td>(.*?)</td>", result_text, re.S)
        Legal_representative = re.findall("法定代表人.*?<span>(.*?)</span>", result_text, re.S)
        Company_address = re.findall("公司地址.*?title=\"(.*?)\">", result_text, re.S)
        industry = re.findall("行业.*?<span>(.*?)</span>", result_text, re.S)
        found_time = re.findall("成立时间.*?<span>(.*?)</span>", result_text, re.S)
        if url_error:
            print(current_time("red").format("url有误，请重试：" + ipc_url))
            print(current_time("sep_suffix"))
            return
        if unit_name:
            print(current_time("green").format("主办单位名称：{}").format(unit_name[0]))
        if industry:
            print(current_time("green").format("行业：{}").format(industry[0]))
        if found_time:
            print(current_time("green").format("成立时间：{}").format(found_time[0]))
        if unit_nature:
            print(current_time("green").format("主办单位性质：{}").format(unit_nature[0]))
        if website_filing:
            print(current_time("green").format("网站备案/许可证号：{}").format(website_filing[0]))
        if website_name:
            print(current_time("green").format("网站名称：{}").format(website_name[0]))
        if Website_owner:
            if not Website_owner[0][0] == "\'":
                print(current_time("green").format("网站负责人：{}").format(Website_owner[0]))
        if Legal_representative:
            print(current_time("green").format("法定代表人：{}").format(Legal_representative[0]))
        if Company_address:
            print(current_time("green").format("公司地址：{}").format(Company_address[0]))
    print(current_time("sep_suffix"))