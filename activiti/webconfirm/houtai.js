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
  password : 'user',
  database : 'exploitAudit'
});
var fs = require('fs');
// 使用session
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
  // 为了让异步的nodejs同步。这么写。resole是正常返回的结果，reject是错误的返回结果。
  // 这个函数执行一个sql语句
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
        // console.log(results)
        resole(JSON.parse((JSON.stringify(results))))
      })
    })
  })
}
// async一定要有，才能使用带promise的函数
async function initinfo(req,res){
  // 读取每个表格，以及每个表格中需要人工授权的host
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
// 提供初始化的数据
app.get('/init', function (req,res){
  initinfo(req, res)
})
// 获取所有的task
function GetListOfTasks(){
  return new Promise((resole,reject)=>{
    request("http://127.0.0.1:8080/activiti-rest/service/runtime/tasks",function(error,response,body){
      resole(JSON.parse(body))
    }).auth("admin","test")
  })
}

async function completework(status,problems,hosts){
  // 先获得所有的task
	var tasks=await GetListOfTasks()
  // 设置好相关参数，result决定了工作流的走向
	var params={"action":"complete","variables":[{"name":"result","value":status}]}
	for( i in tasks["data"]){
		if (tasks["data"][i]["assignee"]=="admin"){
			// 确定身份，发送授权的结果
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
    // 恢复flag
  var update=await exeSql(util.format("update %s set flag=0 where hostid=%s ",problems,hosts))
	}
	

// 这个是用来跳转网页，并记录当时的problems，和host
app.get('/todetail', function (req,res){
  req.session.problems=req.param("problems")
  req.session.hosts=req.param("hosts")
  res.redirect(301,"/detail.html")
})

function sendinfo(res,response){
  // 发送数据
  res.send(response)
}
// 用户对于授权的结果处理函数
app.get('/sendconfirm', function (req,res){
  completework(req.query.status,req.session.problems,req.session.hosts)
  res.send("success")
})

 // 设置监听的端口
var server = app.listen(8085, function () {
  // console.log("应用实例，访问地址为 http://localhost/arista.html",) 
})