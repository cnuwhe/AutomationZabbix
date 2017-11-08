//引入库
var express = require('express');
var app = express();
const path = require('path')
var mysql      = require('mysql');
//定义一个mysql连接池，没有连接池好像会报错
var pool = mysql.createPool({
  host     : 'localhost',
  user     : 'root',
  password : '596100',
  database : 'zabbix'
});
//使用静态页面
app.use(express.static(path.join(__dirname, 'public')));
// 访问这个页面的时候发送这个html
app.get('/arista.html', function (req, res) {
   res.sendFile( __dirname + "/" + "arista.html" );
})
// 访问这个页面的时候发送AiAttack.html
app.get('/AiAttack.html', function (req, res) {
   res.sendFile( __dirname + "/" + "AiAttack.html" );
})


// 页面发送请求的时候到下面这个函数
app.get('/getinfo', function (req, res) {
  // 解析提交的参数
   switch (req.param('selected'))
   {
    case "null":
    response=JSON.stringify("you choose nothing");
    sendinfo(res,response);break;
    case "CPU":
    // 数据库查询操作
    pool.getConnection(function(err, connection){
    connection.query('SELECT clock,value from history where itemid=25462 order by clock DESC limit 100;', 
      function (error, results, fields) {
        if (error) throw error;
        response=JSON.stringify(results)
        // 这里是一个回调函数，这里的赋值在外面不产生影响，所以写个函数把查询结果返回到页面中
        sendinfo(res,response)  
    });
    connection.release();
  });
    break;
    case "Memory":
    // 和上面同理
     pool.getConnection(function(err, connection){
    connection.query('SELECT clock,value from history_uint where itemid=25479 order by clock DESC limit 100;', 
      function (error, results, fields) {
      if (error) throw error;
      response=JSON.stringify(results)
      sendinfo(res,response)
    });
    connection.release();
  });
    break;
    case "login":
    // 和上面同理
     pool.getConnection(function(err, connection){
    connection.query('(SELECT value from history_text where itemid=26100 order by clock DESC limit 1) union (SELECT value from history_text where itemid=26099 order by clock DESC limit 1);', 
      //26100lastb 26099last
      function (error, results, fields) {
      if (error) throw error;
      response=JSON.stringify(results)
      sendinfo(res,response)
    });
    connection.release();
  });
    break;
    default :response=JSON.stringify("nothing");break;
   }
})
app.get('/AI', function (req, res) {
   pool.getConnection(function(err, connection){
  connection.query('SELECT clock,value from history where itemid=25462 order by clock DESC limit 180;', 
      function (error, results, fields) {
        if (error) throw error;
        response=JSON.stringify(results)
        // 这里是一个回调函数，这里的赋值在外面不产生影响，所以写个函数把查询结果返回到页面中
        sendinfo(res,response)  
    });
  connection.release();
  });
})

function sendinfo(res,response){
  // 发送数据
  // console.log(response)
  res.send(response)
}
 // 设置监听的端口
var server = app.listen(8081, function () {
  console.log("应用实例，访问地址为 http://localhost/arista.html",) 
})