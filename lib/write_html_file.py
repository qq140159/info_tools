import re

class Write_Html(object):
    def __init__(self, red_file=None, wri_file=None):
        self.red_file = red_file
        self.wri_file = wri_file

    def write(self):
        with open(self.red_file, "r+", encoding="utf-8") as f:
            result_list = f.readlines()
            
        flag = False
        for i in result_list:
            if "开始目录扫描" in i:
                flag = True
            if flag:
                code = re.findall(".*?http.*?(\d{3})", i, re.S)
                if code:
                    if code[0][0] == "2":
                        result = re.findall("(http.*/).*?(\d.*?)\s.*?title: (.*)", i, re.S)[0]
                        self.write_content("""<a href="{}">{}</a>&emsp;&emsp;{}&emsp;&emsp;{}<br>""".format(result[0],result[0],result[1],result[2].strip()))

                    elif code[0][0] == "3":
                        result = re.findall("(http.*/).*?(\d{3}).*?(=.*?>).*?(http.*?)\s.*?title: (.*)", i, re.S)[0]
                        self.write_content("""<a href="{}">{}</a>&emsp;&emsp;{}&emsp;&emsp;{}&emsp;&emsp;{}&emsp;&emsp;{}<br>""".format(result[0], result[0], result[1],result[2],result[3],result[4].strip()))

                    elif code[0][0] == "4":
                        result = re.findall("(http.*/).*?(\d{3})", i, re.S)[0]
                        self.write_content("""<a href="{}">{}</a>&emsp;&emsp;{}<br>""".format(result[0], result[0], result[1]))

    def write_content(self, content):
        with open(self.wri_file, "a+", encoding="utf-8") as f:
            f.write(content)