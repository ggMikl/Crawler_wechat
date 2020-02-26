from w3lib.html import remove_comments
from w3lib.html import remove_tags_with_content
import re
from zhon.hanzi import punctuation

def suop_to_string(data):
    sring_data = ""
    for item in data:
        sring_data = sring_data + str(item)
    return sring_data

def clear_soup_w3lib(bs4_find_data_group):
    cleared_data_script = remove_tags_with_content(bs4_find_data_group, ('script', 'iframe'))
    cleared_data = remove_comments(cleared_data_script)
    return cleared_data

#去掉特定值
def list_remove_n(l,value):
    j = 0
    for i in range(len(l)):
        if l[j] == value:
            l.pop(j)
        # elif
        else:
            j += 1
    return l

def str_remove_space(str):
    re_str = "".join(str.split())
    return re_str

def str_remove_n(str):
    re_str = str.replace('\n','')
    return re_str

def get_clesr_n(list):
    for i in range(0, len(list)):
        list[i] = str_remove_n(list[i])
    return list

def get_clear_list(list):
    for i in range(0, len(list)):
        list[i] = str_remove_space(list[i])
    return list

def xptha_is_null(list):
    if len(list):
        return list
    else :
        return ['']

def remove_punctuation(line, strip_all=True):
  if strip_all:
    rule = re.compile(r"[^a-zA-Z0-9\u4e00-\u9fa5]")
    line = rule.sub('',line)
  else:
    re_punctuation = "[{}]+".format(punctuation)
    line = re.sub(re_punctuation, "", line)
  return line.strip()
