#2016-10-13 困
#

import json
import urllib.request
url="http://127.0.0.1/zabbix/api_jsonrpc.php"
header={'Content-Type':'application/jsoon'}#只是告诉你这是头部内容


deleteTemplateid="10093"


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

def DisableOneTemplate(auth):#以后hostid也要加上，目前就是个demo，
    data=json.dumps(
   {
    "jsonrpc": "2.0",
    "method": "host.update",#更新
    "params": {
        "hostid":"10084",#制定某个hostid
        "templates_clear":[{"templateid":deleteTemplateid}]#删除哪个模板
    },
    "id": 1,
    "auth": auth
    }
    ).encode()#一定要加这个
    respond=json.loads(sendandget(data))
    return(respond)#返回值不太确定能否看明白是否成功。比较无奈


if __name__ == '__main__':
    auth=login()
    result=DisableOneTemplate(auth)
    print( result)#打印一下结果
   
