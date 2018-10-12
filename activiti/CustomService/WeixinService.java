package Vichy;

import org.activiti.engine.delegate.DelegateExecution;
import org.activiti.engine.delegate.Expression;
import org.activiti.engine.delegate.JavaDelegate;
import org.activiti.engine.impl.util.json.JSONObject;
import org.junit.Test;

import java.util.HashMap;
import java.util.Map;
import java.util.logging.Logger;

public class WeixinService implements JavaDelegate {
    private static final String corpId = "wx869bfa1530302f5";
    private static final String corpSecret = "tfTSUKsayaQnNemNhiT4e3X9K25pcdvzbI8Na_M99gMPMCse0qgW5Dcsh1SLxxD";
    private static final String weixinTokenApi = "https://qyapi.weixin.qq.com/cgi-bin/gettoken";
    private static final String messageApi = "https://qyapi.weixin.qq.com/cgi-bin/message/send";
    private static final String messageBodyTemplate = "{'touser':[],'toparty':'1','msgtype':'text','agentid':2,'safe':0}";

    private static final Logger logger = Logger.getLogger("Vichy.WeixinService");

    private Expression user_param;
    private Expression subject_param;
    private Expression content_param;
    private String user;
    private String subject;
    private String content;
    @Test
    public void test() {
        user = "inforno";
        subject ="123";
        content = "456";

        logger.info("params: [" + user + ", " + subject + ", " + content + "]");
        String accessToken = getToken(corpId, corpSecret);
        sendMessage(accessToken, user, subject, content);
    }    
    @Override
    public void execute(DelegateExecution execution) {
        user = (String) user_param.getValue(execution);
        subject = (String) subject_param.getValue(execution);
        content = (String) content_param.getValue(execution);

        logger.info("params: [" + user + ", " + subject + ", " + content + "]");
        String accessToken = getToken(corpId, corpSecret);
        sendMessage(accessToken, user, subject, content);
    }

    private void sendMessage(String accessToken, String user, String subject, String content) {
        JSONObject messageBody = new JSONObject(messageBodyTemplate);
        Map<String, String> text = new HashMap<>();
        text.put("content", subject + '\n' + content);
        messageBody.put("text", text);
        messageBody.append("touser", user);
        String url = messageApi + "?access_token=" + accessToken;
        logger.info( messageBody.toString());
        HttpClient.sendPost(url, messageBody.toString());
    }

    private String getToken(String corpId, String corpSecret) {
        String tokenUrl = weixinTokenApi + "?corpid=" + corpId + "&corpsecret=" + corpSecret;
        JSONObject res = new JSONObject(HttpClient.sendGet(tokenUrl));
        String token = res.getString("access_token");
        logger.info("token: " + token);
        return token;
    }
}

