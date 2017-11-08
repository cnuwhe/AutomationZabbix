function RawdataToCount(data){
  var date=new Date()
  var map=[new Map(),new Map()]
  for (var j=0;j<data.length;j++)
    {
    var datas=data[j].value.split('\n')
    datas=datas.slice(0,-2)
    for (var i=0;i<datas.length;i++){
    var time=datas[i].split("-")[0].substring(38)+date.getFullYear()

    var mydate=new Date(time).toLocaleString('chinese',{hour12:false})
    console.log(mydate)
    mydate=localeToUTC(mydate)
    if(!map[j].has(mydate)){
      map[j].set(mydate,0)
    }
    map[j].set(mydate,map[j].get(mydate)+1)
   } 
    }
  return map
}

function rawdata(data){
  //这个就是简单的把数据取到，然后按照时间和值画出来。
  data=JSON.parse(data)
  var chart= new Highcharts.Chart('chartcontainer', {          
  chart:  {type: 'line',zoomType: 'x'},
   //指定图表的类型，默认是折线图（line）zoomType‘x’,X轴可以放大
  title: { text: "Arista-"+ $("#selected").val()}, //指定图表标题
  xAxis:{
    type: 'datetime',
    title: {text: null}
    }, //这里是X轴的标记
  yAxis: {
      title: {text: 'value' }  //指定y轴的标题
      },
  series: [{//图中的数值
    data:  objToArrays(data) , 
  name: $("#selected").val()}]
  });
}
function countdata(data){
  data=JSON.parse(data)
  var map=RawdataToCount(data)
  var chart= new Highcharts.Chart('chartcontainer', {          
  chart: {type: 'line'}, //指定图表的类型，默认是折线图（line）
  title: { text: "Arista-"+ $("#selected").val()}, //指定图表标题
  xAxis:{
    type: 'datetime',
    title: {text: null}
    }, //这里是X轴的标记
  yAxis: {
      title: {text: 'count' }  //指定y轴的标题
      },
  series: [//图中的数值
    {name:"success login",
    data:  mapToArrays(map[1]) 
    },
    {name:"fail login",
    data:  mapToArrays(map[0]) 
    }
    ]
  });
}
function submitinfo(){  
 	var showres=document.getElementById("show") 
  $.ajax({  
  url:"/getinfo",  
  type:"get",  
  // data是thetable的值,忘了为啥是这么写,反正是这么写!
  data:$("#thetable").serialize(),  
  cache: false,  
  processData: false,  
  contentType: false,  
  success:function(data){
  switch($("#selected").val())
  {
    case "CPU":
    case "Memory":rawdata(data);showres.value="";break;
    case "login":countdata(data);showres.value="";break;
    default :showres.value=$("#selected").val()
  }
  },  
  error:function(e){  alert("网络错误，请重试！！");  }  
  });         
}  

function mapToArrays(map)
{
  var res=[]
  map.forEach(function(item,key,mapObj){
    res.push([key,item])
  })
  return res
}

function localeToUTC(data)
{
  var date=data.split(' ')[0]
  var time=data.split(' ')[1]
  var year=date.split('/')[0]
  var month=date.split('/')[1]-1
  var day=date.split('/')[2]
  var hour=time.split(':')[0]
  var mintus=time.split(':')[1]
  var second=time.split(':')[2]
  return Date.UTC(year,month,day,hour,mintus,second)
}

function objToArrays(obj)
{
  var res=[]
  for (var each in obj)
  {
    res.push([obj[each].clock*1000,obj[each].value])
  }
  return res
}