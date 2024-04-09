import re
import time


def validateTitle(title):
    re_str = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(re_str, "_", title)  # 替换为下划线
    return new_title


def intToStrTime(a):
    b = time.localtime(a)  # 转为日期字符串
    c = time.strftime("%Y/%m/%d %H:%M:%S", b)  # 格式化字符串
    return c

def unify_duration_format(duar_str_or_s: str):
    """
    01:11 -> 71,'00:01:11'
    00:01:11 -> 71,'00:01:11'
    :param duar_str: '01:11' or '00:01:11'
    :return:  71, '00:01:11'
    """
    error = 0, ''

    def hms(m: int, s: int, h=0):
        if s >= 60:
            m += int(s / 60)
            s = s % 60  #
        if m >= 60:
            h += int(m / 60)
            m = m % 60
        return h * 60 * 60 + m * 60 + s, str(h).zfill(2) + ':' + str(m).zfill(2) + ':' + str(s).zfill(2)

    try:
        s = int(duar_str_or_s)
    except:
        pass
    else:
        return hms(m=s % 3600 // 60, s=s % 60, h=s // 3600)
    try:
        if duar_str_or_s:
            duar_list = duar_str_or_s.split(':')
            if len(duar_list) == 2:
                return hms(m=int(duar_list[0]), s=int(duar_list[1]))
            elif len(duar_list) == 3:
                return hms(m=int(duar_list[1]), s=int(duar_list[2]), h=int(duar_list[0]))
            else:
                return error
        else:
            return error
    except Exception as e:
        return error