import re
from lib.requests_url import get_req
from lib.config import domain_list

def ssl_domain(simple_url):
    query_url = "https://crt.sh/?q={}".format(simple_url)
    content = get_req(query_url).text
    pattern = re.compile(
        "<TD>(\w{0,100}\.\w{0,100}\.?\w{0,100}\.?\w{0,100}\.?\w{0,100}\.?\w{0,100}\.?\w{0,100}\.?\w{0,100})</TD>", re.S)
    if content:
        reg_match(content, pattern)

def reg_match(content, pattern):
    result_list = re.findall(pattern, content)
    if result_list:
        for i in result_list:
            i = re.sub("<b>", "", i.strip())
            if i not in domain_list:
                domain_list.append(i)