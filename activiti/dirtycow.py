import json
import datetime
import pymysql
# 整个脚本用来审核dirtycow漏洞，日志的信息是符合json的标准数据。
# 用于zabbix的自定义监控项。
# 如果数据没有问题，则返回OK，如果有问题则返回相关信息。
db = pymysql.connect("localhost", "root", "wh596100", "zabbix")
db2 = pymysql.connect("localhost", "root", "wh596100", "exploitAudit")
now = datetime.datetime.today()
TIMEOUT = 600


def getdo_sys_open(itemid):
        # 获得do_sys_open函数，timestamp是为了过滤掉返回函数的内容
    cursor = db.cursor()
    cursor.execute(
        "select value from history_log where itemid=%s and \
        value like \"%%do_sys_open%%Timestamp%%\" and value not like\"%%x86_64%%\"order by clock DESC limit 3;" % (itemid))
    data = cursor.fetchall()
    return data


def getvfs_open(file, itemid):
        # 获得vfs_open函数
    cursor = db.cursor()
    exestr = "select value from history_log where itemid=%s and \
        value like \"%%vfs_open%%%s%%\" order by clock DESC limit 1;" % (itemid, file)
    # print(exestr)
    cursor.execute(exestr)
    data = cursor.fetchone()
    return data


def getinode(data):
    data = json.loads(str(data[0]).split('[zabbix]')[1])
    inode = data["parameter"][0]["i_ino"]
    # print(inode)
    return inode


def findWriteBack(inode, itemid):
        # 这个函数用来查找是否存在WriteBack，这个函数本不该出现在一次正常的读写中，
        # 但是它会出现在dirtycow中
    cursor = db.cursor()
    cursor.execute(
        "select value from history_log where itemid=%s and \
        value like \"%%writeback%%%s%%\" order by clock DESC limit 1;" % (itemid, inode))
    data = cursor.fetchone()
    if len(data) != 1:
        return False
    else:
        alterdate = "2018 " + \
            each[0].split('[zabbix]')[0].split(' aq')[0]
        strpdate = datetime.datetime.strptime(alterdate, '%Y %b %d %H:%M:%S')
        # 最后验证一下时间，是不是最近出现在最近
        if (now - strpdate).total_seconds() < TIMEOUT:
            return True
        else:
            return False


def analyseJson(jsons, itemid):
        # 用来分析是否存在dirtycow
    # print(len(jsons))
    for each in jsons:
        each = json.loads(str(each))
        if each["parameter"][1]["value"] != "/proc/self/mem"\
                and each["parameter"][1]["value"] != "/etc/ld.so.cache":
                # 这两个不是我们需要的参数，去掉。
            res = bin(each["parameter"][2]["value"])[-2:]
            if res == "00":
                # 读取最后两位，并看着是不是00（00读取），dirtycow正是利用读取完成复写的。
                # each["parameter"][1]["value"]是被操作的文件。
                data = getvfs_open(each["parameter"][1]["value"], itemid)
                # 利用inode来找回写函数。
                inode = getinode(data)
                # print(inode)
                if findWriteBack(inode, itemid):
                        # 在这里可以延伸一下，查询更多的信息。
                    return each["parameter"][1]["value"] +\
                        "  has illegally written back"
                else:
                    return "OK"
            else:
                return "OK"


def getallhosts():
        # 获得所有的hosts
    cursor = db2.cursor()
    cursor.execute("select logitem,hostid from dirtycow ")
    data = cursor.fetchall()
    return data


if __name__ == '__main__':
    hosts = getallhosts()
    result = []
    if len(hosts) > 0:
        for eachhost in hosts:
                # 对每个host进行dirtycow检查
            historys = getdo_sys_open(eachhost[0])
            jsons = []
            if len(historys) < 3:
                # 我们发现发送dirtycow时会产生三个do_sys_open，所以少于三个时可以并不考虑
                print('OK')
                exit()
            for each in historys:
                alterdate = "2018 " + \
                    each[0].split('[zabbix]')[0].split(' aq')[0]
                strpdate = datetime.datetime.strptime(
                    alterdate, '%Y %b %d %H:%M:%S')
                # 计算时间差，时间差小于timeout的日志不再进行审查
                # print((now - strpdate).total_seconds())
                if (now - strpdate).total_seconds() < TIMEOUT:
                    jsons.append(each[0].split('[zabbix]')[1])
            if len(jsons) < 3:
                # 如果少于3个符合条件的do_sys_opne依旧不用检查
                print('OK')
            else:
                # 现在开始审查
                eachresult = (analyseJson(jsons, eachhost[0]))
                if eachresult != 'OK':
                        # 如果出现了问题，返回相关信息。
                    result.append(str(eachhost[1]) + ":" + eachresult)
        if len(result) > 0:
            print(result)
    else:
        print('OK')
