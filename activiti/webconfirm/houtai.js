//引入库
var express = require('express');
var app = express();
var session=require('express-session');
var request=require('request');
const path = require('path');
var mysql = require('mysql');
var util=require('util')
// var bodyparser=
//定义一个mysql连接池，没有连接池好像会报错
var pool = mysql.createPool({
  host     : 'localhost',
  user     : 'root',
  password : 'wh596100',
  database : 'exploitAudit'
});
var fs = require('fs');
app.use(session({
    secret: '1122334455', //secret的值建议使用随机字符串
    cookie: {maxAge: 60 * 1000}, // 过期时间（毫秒）
    resave:false,
    saveUninitialized:true
}));
//使用静态页面
app.use(express.static(path.join(__dirname, 'public')));
// 访问这个页面的时候发送这个html

function exeSql(line){
  return new Promise((resole,reject) => {
    pool.getConnection((err,connection) => {
      if (err){
        reject(err)
      }
      connection.query(line,(err,results,fields) =>
      {
        if (err){
          reject(err)
        }
        try{
          resole(JSON.parse((JSON.stringify(results))))
        }
        catch(err){}
      })
    })
  })
}

async function initinfo(req,res){
  var hosts=new Object()
  results = await exeSql('show tables')
  for (each in results){
    eachResults=await exeSql(util.format("select hostid,name from zabbix.hosts where hostid=(select hostid from %s where flag =1)",results[each]["Tables_in_exploitAudit"]))
    hosts[results[each]["Tables_in_exploitAudit"]]=eachResults
    // name= await exeSql(util.format("select name from hosts where hostid=%s",))
  }
  // console.log(hosts)
  res.send(JSON.stringify(hosts))
}
app.get('/init', function (req,res){
  initinfo(req, res)
})

function GetListOfTasks(){
  return new Promise((resole,reject)=>{
    request("http://127.0.0.1:8080/activiti-rest/service/runtime/tasks",function(error,response,body){
      resole(JSON.parse(body))
    }).auth("admin","test")
  })
}
async function completework(status,problems,hosts){
	var tasks=await GetListOfTasks()
  // console.log(status,problems,hosts)
  var update=await exeSql(util.format("update %s set flag=0 where hostid=%s ",problems,hosts))
	var params={"action":"complete","variables":[{"name":"result","value":status}]}
	for( i in tasks["data"]){
		if (tasks["data"][i]["assignee"]=="admin"){
			// console.log(params)
				var aaa=request({
			    url: tasks["data"][i]["url"],
			    method: "POST",
			    headers: {"content-type": "application/json",},
			    auth:{
			    'user': 'admin',
			    'pass': 'test',
			    'sendImmediately': false},
			    body: JSON.stringify(params)},function(err,req,body){
			    	console.log(body)
			    }); 
      }
		}
	}

app.get('/endWorkFlow', function (req,res){
  endWorkFlow()
  res.send("success")
})

async function endWorkFlow(){
  var tasks=await GetListOfTasks()
  var params={"action":"complete"}
  for( i in tasks["data"]){
    if (tasks["data"][i]["assignee"]=="admin"){
        var aaa=request({
          url: tasks["data"][i]["url"],
          method: "POST",
          headers: {"content-type": "application/json",},
          auth:{
          'user': 'admin',
          'pass': 'test',
          'sendImmediately': false},
          body: JSON.stringify(params)},function(err,req,body){
            console.log(body)
          }); 
      }
    }
  }

function zabbixlogin()
{return new Promise((resole,reject)=>{
     var data={"jsonrpc": "2.0",
        "method": "user.login",  
        "params": {
            "user": "Admin",
            "password": "wh596100"
        },
        "id": 10 }

     var aaa=request({
          url: "http://127.0.0.1/zabbix/api_jsonrpc.php",
          method: "POST",
          headers: {"content-type": "application/json",},
          body: JSON.stringify(data)},function(err,req,body){
               if(err){reject(err)}
            resole(JSON.parse(body)["result"])
          }); 

})}
function reporter(token,hostid){
     return new Promise((resole,reject)=>{
var data={"jsonrpc": "2.0",
        "method": "script.execute",  
        "params": {
            "scriptid": "11",
            "hostid": hostid
        },
        "id": 10,
        "auth": token}
var aaa=request({
          url: "http://127.0.0.1/zabbix/api_jsonrpc.php",
          method: "POST",
          headers: {"content-type": "application/json",},
          body: JSON.stringify(data)},function(err,req,body){
               if(err){reject(err)}
            resole(JSON.parse(body)["result"])
          }); 
     })}
async function report(hostid,res){
     var token=await zabbixlogin()
     var result=await reporter(token,hostid)
     res.send(JSON.stringify(result))
}


app.get('/todetail', function (req,res){
  // console.log(req.querys.problems)
  req.session.problems=req.query.problems
  req.session.hosts=req.query.hosts
  res.redirect(302,"/detail.html")
})
function sendinfo(res,response){
  // 发送数据
  // console.log(response)
  res.send(response)
}
app.get('/sendconfirm', function (req,res){
  // console.log(req.query.status,req.session.problems,req.session.hosts)
  completework(req.query.status,req.session.problems,req.session.hosts)
  res.send("success")
})
app.get('/report', function (req,res){
  console.log(req.query.hostid)
  report(req.query.hostid,res)
})

 // 设置监听的端口
var server = app.listen(8085, function () {
  // console.log("应用实例，访问地址为 http://localhost/arista.html",) 
})