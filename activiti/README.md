#环境：
nodejs版本 v8.6
python版本 v3.5.2
#安全：
个人密码全部都删除了。所以直接clone是不能运行的。

#CustomService
存放的是java代码，用到activiti工作流中。这是两个包。我只把代码放进去了。
代码实现的功能是运行zabbix指定脚本、修改zabbix指定监控项状态、初始化变量，以及发送微信。
CustomServiceinZabbix.jar是我实现后导出的包。存入tomcat/webapps/activiti-rest(app)/WEB-INFO/lib

#webconfirm
存放的是nodejs代码，实现了一个小网站，用于进行人工确认。

#几个python程序的用途。
confirmtask用于确认一个工作流任务，放在zabbix的响应动作中。
dirtycow被用做一个自定义监控项，用于确认dirtycow被触发了。同理overlayMysql
reporter需要放在被监控节点，并设置一个zabbix预设脚本去启动，它用于获取用户的操作记录。
workflowstarter是工作流的启动脚本，放在zabbix的响应动作中。

