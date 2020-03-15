import re
from lib.requests_url import post_req
from lib.config import domain_list

def nsdumpster_com(simple_url):
    query_url = "https://dnsdumpster.com/"
    cookie = "csrftoken=RdP7etdRrzORPXde6hj58NnJipVdqfCUiJdk0OlQk7LKrigKukARxRneZHmmiD78; _ga=GA1.2.329292680.1582810390; _gid=GA1.2.1253419315.1582810390;"
    cookie_dict = {i.split("=")[0]: i.split("=")[-1] for i in cookie.split("; ")}
    data = {
        "csrfmiddlewaretoken": "9WQcyrINDgydlBwCLSExNPYjX9dK4ghiAsepkMQMwOv6XWz89VVjcTYOErETWEMw",
        "targetip": simple_url,
    }
    content = post_req(query_url, data=data, cookies=cookie_dict).text
    pattern = re.compile("""<tr><td class="col-md-4">(.*?)<""", re.S)
    if content:
        reg_match(content, pattern)

def reg_match(content, pattern):
    result_list = re.findall(pattern, content)
    if result_list:
        for i in result_list:
            i = i.strip()
            if i not in domain_list and i[-1] != ".":
                domain_list.append(i)
