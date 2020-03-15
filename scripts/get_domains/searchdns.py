import re
from lib.requests_url import get_req
from lib.config import domain_list


def searchdns_netcraft_com(simple_url):
    query_url = "https://searchdns.netcraft.com/?restriction=site+contains&host={}&position=limited".format(simple_url)
    cookie = "netcraft_js_verification_challenge=djF8RUlTNmw3d3c3M2c1WlNOOWZ0UHBMOTNPZ3YzWmVjY0tXWDBnUm9xSEFid1c4dEtOcjNoTHRp%0AaTRUWTBxUTBZOHo2NkFUbEtGdlpnSQovanQ5eStTditRPT0KfDE1ODI4MTU5Mzc%3D%0A%7Cab7e7165c79edb9371c422b504bf4cdd28713046; netcraft_js_verification_response=957f5bb05b956dbd8a1790ae4529e9ad0e0b6eb2"
    cookie_dict = {i.split("=")[0]: i.split("=")[-1] for i in cookie.split("; ")}
    content = get_req(query_url, cookies=cookie_dict).text
    pattern = re.compile("""rel="nofollow">.*?(\w{0,100}\..*?<b>.*?)</b>""", re.S)
    if content:
        reg_match(content, pattern)

def reg_match(content, pattern):
    result_list = re.findall(pattern, content)
    if result_list:
        for i in result_list:
            i = re.sub("<b>", "", i.strip())
            if i not in domain_list:
                domain_list.append(i)
