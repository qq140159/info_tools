from time import strftime, localtime
import datetime,time

redirect_list = []
response_code = [0]
domain_list = []
char_set = ['\\', '|', '/', '-']
censys_api_id = ""
censys_api_secret = ""

def current_time(color):
    if color == "red":
        return "\033[1;31;40m[!!!]%s{}\033[1m" % (strftime("%Y-%m-%d %H:%M:%S", localtime()) + "   ")
    elif color == "green":
        return "\033[1;32;40m[+]%s{}\033[1m" % (strftime("%Y-%m-%d %H:%M:%S", localtime()) + "   ")
    elif color == "yellow":
        return "\033[1;33;40m[!]%s{}\033[1m" % (strftime("%Y-%m-%d %H:%M:%S", localtime()) + "   ")
    elif color == "blue":
        return "\033[1;34;40m[*]%s{}\033[0m" % (strftime("%Y-%m-%d %H:%M:%S", localtime()) + "   ")
    elif color == "sep_prefix":
        return current_time("blue").format("-" * 80)
    elif color == "sep_suffix":
        return current_time("blue").format("-" * 80 + "\r\n")











