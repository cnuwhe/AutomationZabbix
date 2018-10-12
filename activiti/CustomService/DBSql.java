package Vichy;

import java.sql.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.logging.Logger;

public class DBSql {
    private static final String driver = "com.mysql.jdbc.Driver";
    private static final String db = "jdbc:mysql://localhost:3306/exploitAudit";
    private static final String username = "root";
    private static final String password = "password";

    private static final Logger logger = Logger.getLogger("Vichy.DBSql");

    public static Connection connect() {
        try {
            Class.forName(driver);
            Connection con = DriverManager.getConnection(db, username, password);
            if (!con.isClosed()) {
                logger.info("connect db succeed");
                return con;
            }
            logger.warning("connect db failed");
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
            logger.warning("can't find driver");
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return null;
    }

    public static void disconnect(Connection conn) {
        try {
            conn.close();
            logger.info("connect closed");
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public static List<Map<String, Object>> query(String sql) {
        List<Map<String, Object>> re = new ArrayList<>();

        Connection db = connect();
        if (db != null) {
            try {
                Statement statement = db.createStatement(ResultSet.TYPE_SCROLL_INSENSITIVE, ResultSet.CONCUR_READ_ONLY);
                ResultSet results = statement.executeQuery(sql);
                while(results.next()) {
                    Map<String, Object> row = new HashMap<>();
                    ResultSetMetaData resultSetMetaData = results.getMetaData();
                    for (int i = 1, length = resultSetMetaData.getColumnCount(); i <= length; i++) {
                        row.put(resultSetMetaData.getColumnName(i), results.getObject(i));
                    }
                    re.add(row);
                }
                statement.close();
            } catch (SQLException e) {
                e.printStackTrace();
            } finally {
               
                disconnect(db);
            }
        }
        return re;
    }

    public static List<Map<String, Object>> query(String sqlTemplate, Object... args) {
        return query(String.format(sqlTemplate, args));
    }

    public static int update(String sql) {
        Connection db = connect();
        int effectRows = 0;
        if (db != null) {
            try {
                Statement statement = db.createStatement(ResultSet.TYPE_SCROLL_INSENSITIVE, ResultSet.CONCUR_UPDATABLE);
                effectRows = statement.executeUpdate(sql);
                logger.info("effect row: " + effectRows);
                statement.close();
            } catch (SQLException e) {
                e.printStackTrace();
            } finally {
                disconnect(db);
            }
        }
        return effectRows;
    }

    public static int update(String sqlTemplate, Object... args) {
        return update(String.format(sqlTemplate, args));
    }
}
