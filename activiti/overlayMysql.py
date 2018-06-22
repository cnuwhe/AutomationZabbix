import json
import datetime
import pymysql
# overlayfs漏洞审查函数，在zabbix 中作为自定义监控存在。
# 正常返回OK，不正常返回相关内容。


def gethistory():
    # 查找ovl_setattr函数
    db = pymysql.connect("localhost", "root", "wh596100", "zabbix")
    cursor = db.cursor()
    cursor.execute(
        "select value from history_log where itemid=26218 and \
        value like \"%%ovl_setattr%%\" order by clock DESC limit 2;")
    data = cursor.fetchall()
    return data


def analyseJson(jsons):
    if len(jsons) == 2:
        # print(jsons[0])
        returndata = json.loads(str(jsons[0]))
        # print(returndata['returnValue'])
        predata = json.loads(str(jsons[1]))
        # print(predata['task_struct']['uid'])
        for each in predata['parameter']:
            if each['type'] == 'dentry inode':
                # 好像是这里有问题，才提权的，为啥我忘了。emmm
                # print(each['uid'])
                inode = str(each['uid'])
        return "An ordinary process with a pid of " + str(predata['task_struct']['uid']) + " illegally modifies the root file"


if __name__ == '__main__':
    historys = gethistory()
    jsons = []
    now = datetime.datetime.today()
    # print(now)
    for each in historys:
        alterdate = "2018 " + \
            each[0].split('[zabbix]')[0].split(' aq')[0]
        strpdate = datetime.datetime.strptime(alterdate, '%Y %b %d %H:%M:%S')
        # 计算时间差，超过一定时间的我不再审核。
        # print((now - strpdate).total_seconds())
        if (now - strpdate).total_seconds() < 120:
            jsons.append(each[0].split('[zabbix]')[1])
    if len(jsons) <= 1:
        print('OK')
    else:
        # 正式的审核函数。
        print(analyseJson(jsons))
