#2016-9-29快国庆啦～
#开始吐槽我这一下午的工作。。。。。。

import json
import urllib.request

url="http://127.0.0.1/zabbix/api_jsonrpc.php"
header={'Content-Type':'application/jsoon'}#只是告诉你这是头部内容
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
).encode()#一定要加这个，不加这个服务器无法解析。

if __name__ == '__main__':
    #d=urllib.parse.quote(data).encode('UTF8')，这个是错的。虽然和上面一样都是encode，但是这样就是错的，不要问为什么！我也不知道！
    logrequest=urllib.request.Request(url,data, {'Content-Type': 'application/json'})#最后一个参数是头部。我来组成头部，哈哈哈哈
    try:
        result=urllib.request.urlopen(logrequest)
    except urllib.error.URLError as e:
        print("error:"+str(e.code))
    else:
        response=json.loads(result.read().decode('UTF-8'))
        result.close()
        print(response)
        print (response.get("result"))
