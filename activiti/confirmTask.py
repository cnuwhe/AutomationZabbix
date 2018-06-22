import json
import urllib.request
import sys
# 这个脚本用于在进一步审核中，zabbix向工作流返回确认信息，代表的确发现了什么。
ActivitiUrl = "http://localhost:8080/activiti-rest/service/runtime/tasks"
header = {'Content-Type': 'application/json'}


def SendToActiviti(url, data):  # 发送数据并接收结果，但好像也没什么结果
    Arequest = urllib.request.Request(
        url, data, header)
    try:
        result = urllib.request.urlopen(Arequest)
    except urllib.error.URLError as e:
        print("error:" + str(e.code))
    else:
        returnvalue = result.read().decode('UTF-8')
        result.close()


def getinformation(theurl):
    # Y用来从activiti获取一些信息。
    Arequest = urllib.request.Request(url=theurl, headers=header)
    result = urllib.request.urlopen(Arequest)
    jsonres = json.loads(result.read().decode())
    result.close()
    return jsonres


def confirmglobalparams(url, hosts):
    theurl = url + "/variables"
    #获取每个工作流实例的参数。
    params = getinformation(theurl)
    for each in params:
        # 对比hostid，通过hostid来确定唯一的工作流实例。
        if each["name"] == "hostid" and \
                each["value"] in hosts:
            return True
    return False


def GetTaskList():
    # 获得所有给zabbix用户的tasks
    taskList = getinformation(ActivitiUrl)
    resurl = []
    hosts = []
    # sys.argv[1][1:-1].split(",")用来找到所有的审核结果。
    for each in sys.argv[1][1:-1].split(","):
        hosts.append(each.split(":")[0].strip())
    for each in taskList["data"]:
        # 找通过参数来确认要完成哪个任务。
        for eachhost in hosts:
            if each["assignee"] == "zabbix" and confirmglobalparams(each["url"], eachhost):
                return each["url"]


if __name__ == '__main__':
    password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, ActivitiUrl, 'zabbix', 'zabbix')
    # 这几步主要用于加验证身份。
    handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
    opener = urllib.request.build_opener(handler)
    urllib.request.install_opener(opener)
    # 之后的request都会加上这个身份验证。
    # 获取所有的给zabbix用户的任务。
    url = GetTaskList()
    # print("success")
    data = json.dumps({"action": "complete"}).encode()
    # 发送完成任务请求。
    SendToActiviti(url, data)
