from scripts.get_domains.nsdum import nsdumpster_com
from scripts.get_domains.searchdns import searchdns_netcraft_com
from scripts.get_domains.censys_ import censys_subdomains
from scripts.get_domains.ssl_ import ssl_domain
from lib.config import domain_list,current_time
import datetime

def domain_main(domain):
    domain = domain[domain.find(".") + 1:]
    print(current_time("yellow").format("开始域名扫描..."))
    print(current_time("sep_prefix"))
    st = datetime.datetime.now()

    ssl_domain(domain)
    nsdumpster_com(domain)
    searchdns_netcraft_com(domain)
    censys_subdomains(domain)

    for i in domain_list:
        print(current_time("green").format(i))

    print(current_time("yellow").format("域名扫描耗时:" + str((datetime.datetime.now() - st).total_seconds()) + "秒"))
    print(current_time("sep_suffix"))









