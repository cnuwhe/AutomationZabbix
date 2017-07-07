import json
import urllib.request
import sys
url = "http://127.0.0.1/zabbix/api_jsonrpc.php"


def sendandget(data):  # 发送数据并接收
    logrequest = urllib.request.Request(
        url, data, {'Content-Type': 'application/json'})
    # 最后一个参数是头部。我来组成头部，哈哈哈哈
    try:
        result = urllib.request.urlopen(logrequest)
    except urllib.error.URLError as e:
        print("error:" + str(e.code))
    else:
        returnvalue = result.read().decode('UTF-8')
        result.close()
    return (returnvalue)


if __name__ == '__main__':
    auth = sys.argv[1]
    state=sys.argv[2]
    #auth = "c9043d0e8090741dfbd345ef7108bf44"
    data = json.dumps({
        "jsonrpc": "2.0",
        "method": "item.update",  # item update
        "params": {
            "itemid": "23845",
            "status": state
# 0 is on; 1 is off
        },
        "id": 1,
        "auth": auth
    }).encode()
    respond = json.loads(sendandget(data))
    # print(respond)
