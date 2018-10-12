import json
import urllib.request
import sys
import pymysql
# 工作流启动脚本。在zabbix作为动作启动。
ActivitiUrl = "http://127.0.0.1:8080/activiti-rest/service/runtime/process-instances"
# 要安装activiti-rest。上面那个是rest的地址。可以获得所有的启动实例。具体的去看官方说明。
header = {'Content-Type': 'application/json'}
db = pymysql.connect("localhost", "root", "wh596100", "exploitAudit")
db2 = pymysql.connect("localhost", "root", "wh596100", "zabbix")


def updateflag(hostid, exploit): 、
# 有个表，表中flag代表是否需要人工授权。更新里面的flag。代表需要授权
# 查找有多少个itemid需要携带。
    cursor = db.cursor()
    cursor.execute("update %s set flag=1 where hostid=%s" % (exploit, hostid))
    db.commit()
    cursor.execute("select items from %s where hostid=%s" % (exploit, hostid))
    data = cursor.fetchone()
    # print(data)
    return data


def gethostid(hostname):
    # 启动参数只能用hostname，但是在工作流中多处需要hostid，所以我们使用hostid而不是hostname。
    cursor = db.cursor()
    # print(hostname)
    cursor.execute(
        "select hostid from zabbix.hosts where name='" + hostname + "';")
    data = cursor.fetchone()
    print(data[0])
    return data[0]


def SendToActiviti(data):  # 发送数据并接收
    Arequest = urllib.request.Request(
        ActivitiUrl, data, header)
    # 发送启动工作流请求
    try:
        result = urllib.request.urlopen(Arequest)
    except urllib.error.URLError as e:
        print("error:" + str(e.code))
    else:
        returnvalue = result.read().decode('UTF-8')
        result.close()
    return returnvalue


if __name__ == '__main__':
    start = {}
    start["processDefinitionId"] = sys.argv[1]
    # 流程定义ID
    start["businessKey"] = sys.argv[2]
    # businessKey这两个是用来启动指定工作流的。
    start["variables"] = []
    # 用来携带一些参数。参数包括hostid，和工作流中需要使用的itemid等。
    hostid = gethostid(sys.argv[3])
    start["variables"].append({"name": "hostid", "value": str(hostid)})
    # i = 1
    # for each in updateflag(hostid, sys.argv[4])[0].split(":"):
    #     # 把itemid当作参数带入到工作流中
    #     start["variables"].append({"name": "item" + str(i), "value": each})
    #     i = i + 1
    password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, ActivitiUrl, 'admin', 'test')
    handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
    # 这几步主要用于加验证身份。admin是用户名，test是密码。
    opener = urllib.request.build_opener(handler)
    urllib.request.install_opener(opener)
    # 之后的request都会加上这个身份验证。
    data = json.dumps(start).encode()  # 一定要加这个，不加这个服务器无法解析。。
    # # print(data)
    respond = json.loads(SendToActiviti(data))
    print(respond)
