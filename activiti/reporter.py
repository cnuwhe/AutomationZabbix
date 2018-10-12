import json
import urllib.request
import sys
import os
ActivitiUrl = "http://192.168.1.129:8080/activiti-rest/service/runtime/process-instances"
header = {'Content-Type': 'application/json'}


def getinformation(theurl):
    Arequest = urllib.request.Request(url=theurl, headers=header)
    result = urllib.request.urlopen(Arequest)
    jsonres = json.loads(result.read().decode())
    result.close()
    return jsonres


if __name__ == '__main__':
    password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, ActivitiUrl, 'admin', 'test')
    handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
    opener = urllib.request.build_opener(handler)
    urllib.request.install_opener(opener)
    uid=-1
    taskList = getinformation(ActivitiUrl)["data"]
    for each in taskList:
        params = getinformation(str(each["url"]) + "/variables")
        flag=0
        tmpuid=-1
        for eachp in params:
            if eachp["name"]=="uid":
                print(eachp["value"])
                tmpuid=eachp["value"]
            if eachp["value"] == "10120" and eachp["name"]=="hostid":
                flag=1
            if flag==1 and tmpuid!=-1:
                uid=int(tmpuid)
    if uid!=-1:
	    f = open("/etc/passwd", "r")
	    for eachline in f.readlines():
	        if eachline.split(":")[2] == str(uid):
	            name=eachline.split(":")[0]
	            break
	    f=open("/home/"+name+"/.bash_history")
	    result=f.readlines()
	    print(result)
	    login=os.popen("last")
	    for line in login.readlines():
	        if line.find(name)!=-1:
	            print(line)
    else:
        print("uid wrong")