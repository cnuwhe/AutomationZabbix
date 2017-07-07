import os
import json
if __name__ == '__main__':
    res = os.popen('sudo /home/tsinghua/kweb/Arsenal/nettop.stp').readlines()
    if len(res) > 11:
        # print(res[1:10])
        data = res[1:10]
    else:
        # print(res)
        data = res
    Adict = {}
    Adict["head"] = "incoming flood"
    Adict["problem"] = "download speed is over 1M/S"
    Adict["detail"] = "download speed is over 1M/S"
    Adict["count"] = len(data)
    i = 1
    for each in data:
        each = each.strip()
        pid = "pid" + str(i)
        Adict[pid] = each
        i = i + 1
    f = open("/home/tsinghua/kweb/html/test.json", "w")
    tojson = json.dumps(Adict, ensure_ascii=False)
    f.write(str(tojson))
    print(data[1])
