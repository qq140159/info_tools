import argparse
import sys

def parse_args():
    parser = argparse.ArgumentParser(description="我的信息收集神器...")
    parser.add_argument('-a', '--all', help="扫描所有...", default=False, action="store_true")
    parser.add_argument('-t', '--thread', type=int, default=100, help="线程数量,默认100线程")
    parser.add_argument('-u','--url', type=str, help="添加url链接")
    parser.add_argument('-U', '--Url_file', help="添加一个url文件")
    parser.add_argument('-w', '--whois',  help="whois查询", default=False, action="store_true")
    parser.add_argument('-i', '--ipc', help="ipc备案查询", default=False, action="store_true")
    parser.add_argument('-y', '--yunsee', help="云悉指纹查询", default=False, action="store_true")
    parser.add_argument('-n', '--nmap', help="nmap扫描", default=False, action="store_true")
    parser.add_argument('-d', '--dir', help="dir扫描", default=False)
    parser.add_argument('-s', '--sub_domain', help="扫描子域名", default=False, action="store_true")

    args = parser.parse_args()
    if not args.url and not args.Url_file or len(sys.argv) < 4:
        parser.print_help()
        sys.exit(0)
    return args


