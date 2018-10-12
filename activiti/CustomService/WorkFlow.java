package Vichy;

import org.activiti.engine.delegate.DelegateExecution;
import org.activiti.engine.delegate.Expression;
import org.activiti.engine.delegate.JavaDelegate;
import org.activiti.engine.impl.util.json.JSONArray;
import org.activiti.engine.impl.util.json.JSONObject;

import java.util.List;
import java.util.Map;

public class WorkFlow implements JavaDelegate {
    private Expression hostid_param;
    private Expression exploit_param;
    private String hostid;
    private String exploit;

    @Override
    public void execute(DelegateExecution execution) {
        hostid = (String) hostid_param.getValue(execution);
        exploit = (String) exploit_param.getValue(execution);
        String[] items = updateFlag(hostid, exploit).split(":");
        JSONObject start =  genVariables(items);
        execution.setVariable("items", start.toString());

    }

    private JSONObject genVariables(String[] items) {
        JSONObject variables = new JSONObject();
        for(int i = 0, length = items.length; i < length; i++) {
            variables.put("item"+ String.valueOf(i), items[i]);
        }
        return variables;
    }

    private String updateFlag(String hostid, String exploit) {
        DBSql.update("update %s set flag=1 where hostid=%s", exploit, hostid);
        List<Map<String, Object>> result = DBSql.query("select items from %s where hostid=%s limit 1", exploit, hostid);
        return (String) result.get(0).get("items");
    }
}
