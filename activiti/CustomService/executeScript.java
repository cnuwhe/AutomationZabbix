package CustomService;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;

import org.activiti.engine.delegate.DelegateExecution;
import org.activiti.engine.delegate.Expression;
import org.activiti.engine.delegate.JavaDelegate;
import org.activiti.engine.impl.util.json.JSONObject;

public class executeScript implements JavaDelegate{
	  private Expression param1;
	  private Expression param2;
	public String login() {
		JSONObject object=new JSONObject();
		object.put("jsonrpc","2.0");
		object.put("method","user.login");
		object.put("id", 2);
		JSONObject params=new JSONObject();
		params.put("user", "Admin");
		params.put("password", "password");
		object.put("params", params);
		String loginJSON =object.toString();
//		System.out.println(loginJSON);
		return loginJSON;
	}
	
	public String executeScript(String token,String sciptid,String hostid) {
		JSONObject object=new JSONObject();
		object.put("jsonrpc","2.0");
		object.put("method","script.execute");
		object.put("id", 2);
		object.put("auth", token);
		JSONObject params=new JSONObject();
		params.put("scriptid", sciptid);
		params.put("hostid", hostid);
		object.put("params", params);
		String res =object.toString();
//		System.out.println(res);
		return res;
	}
	
	public String logout(String token) {
		JSONObject object=new JSONObject();
		object.put("jsonrpc","2.0");
		object.put("method","user.logout");
		object.put("id", 2);
		object.put("auth", token);
		JSONObject params=new JSONObject();
		object.put("params", params);
		String loginJSON =object.toString();
//		System.out.println(loginJSON);
		return loginJSON;
	}

	public  String sendPost(String Params) {
		 OutputStreamWriter out = null;
	        BufferedReader reader = null;
	        String response="";
	        try {
	            URL httpUrl = null; //HTTP URL�� �����������������
	            //����URL
	            httpUrl = new URL("http://127.0.0.1/zabbix/api_jsonrpc.php");
	            //��������
	            HttpURLConnection conn = (HttpURLConnection) httpUrl.openConnection();
	            conn.setRequestMethod("POST");
	            conn.setRequestProperty("Content-Type", "application/json");
	            conn.setUseCaches(false);//���ò�Ҫ����
	            conn.setInstanceFollowRedirects(true);
	            conn.setDoOutput(true);
	            conn.setDoInput(true);
	            conn.connect();
	            //POST����
	            out = new OutputStreamWriter(
	                    conn.getOutputStream());
	            out.write(Params);
	            out.flush();
	            //��ȡ��Ӧ
	            reader = new BufferedReader(new InputStreamReader(
	                    conn.getInputStream()));
	            String lines;
	            while ((lines = reader.readLine()) != null) {
	                lines = new String(lines.getBytes(), "utf-8");
	                response+=lines;
	            }
	            reader.close();
	            // �Ͽ�����
	            conn.disconnect();

//	            System.out.println(response.toString());
	        } catch (Exception e) {
	        System.out.println("���� POST ��������쳣��"+e);
	        e.printStackTrace();
	        }
	        //ʹ��finally�����ر��������������
	        finally{
	        try{
	            if(out!=null){
	                out.close();
	            }
	            if(reader!=null){
	                reader.close();
	            }
	        }
	        catch(IOException ex){
	            ex.printStackTrace();
	        }
	    }

	        return response;
	}

	@Override
	//�ⲿ��ֻ����ôд��
	public void execute(DelegateExecution arg0) {
		String scriptid=(String)param1.getValue(arg0);
		String hostid=(String)param2.getValue(arg0);
		JSONObject token=new JSONObject(sendPost(login()));
		String auth=token.get("result").toString();
		String result=sendPost(executeScript(auth,scriptid , hostid));
		System.out.println(result);
		sendPost(logout(auth));
	}
}
