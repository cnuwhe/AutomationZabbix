#2016-10-13感觉身体被掏空
#

import json
import urllib.request
url="http://127.0.0.1/zabbix/api_jsonrpc.php"
header={'Content-Type':'application/jsoon'}#只是告诉你这是头部内容

NewTemplate=[{"templateid":"10093"}]#数列

def login():#登陆函数，其实就是构造了一个json
    data=json.dumps(
    {
    "jsonrpc":"2.0",
    "method":"user.login",#喏……我要登录了
    "params":{
        "user":"Admin",
        "password":"zabbix"
    },
    "id": 1#这个传说随便写
    }
    ).encode()#一定要加这个，不加这个服务器无法解析。。
    respond=json.loads(sendandget(data))
    return(respond.get("result"))#返回值为授权码


def sendandget(data):#发送数据并接收
    logrequest=urllib.request.Request(url,data, {'Content-Type': 'application/json'})#最后一个参数是头部。我来组成头部，哈哈哈哈
    try:
        result=urllib.request.urlopen(logrequest)
    except urllib.error.URLError as e:
        print("error:"+str(e.code))
    else:
        returnvalue=result.read().decode('UTF-8')
        result.close()
    return (returnvalue)

def getTemplate(auth):#以后hostid也要加上，目前就是个demo，
    data=json.dumps(
   {
    "jsonrpc": "2.0",
    "method": "host.get",#获取某hostid的所有模板
    "params": {
        "output": ["hostid"],
        "selectParentTemplates": [
            "templateid",
            "name"
        ],
        "hostids": "10084"#以后这个要改成参数
    },
    "id": 1,
    "auth": auth
    }
    ).encode()#一定要加这个
    respond=json.loads(sendandget(data))['result'][0]['parentTemplates']#字典-数列-字典（环环嵌套。。。。）
    return(respond)#返回值为当前hostid所有连接的模板

def updateTemplate(NewTemplate,auth):
    data=json.dumps(
    {
    "jsonrpc": "2.0",
    "method": "host.update",#开始要更新啦
    "params": {
        "hostid":"10084",
        "templates":NewTemplate#因为是复写，所以要有原本的模板和新的模板
        },
    "id": 1,
    "auth": auth
    }
    ).encode()#一定要加这个
    respond=json.loads(sendandget(data))
    return(respond)

if __name__ == '__main__':
    auth=login()
    templatedlist=getTemplate(auth)
    #print( templatedlist)
    for template in templatedlist:
        print (template['templateid'],template['name'])#打印目前有的模板
        tempdict={"templateid":template['templateid']}#构造模板格式
        NewTemplate.append(tempdict)#数列增加
    print(updateTemplate(NewTemplate,auth))

      

