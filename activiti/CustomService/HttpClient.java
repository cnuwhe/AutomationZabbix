package Vichy;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.logging.Logger;

public class HttpClient {
    public static final String method = "POST";
    public static final String contentType = "application/json";
    public static final Boolean cache = false;

    private static final Logger logger = Logger.getLogger("Vichy.HttpClient");

    public static String sendGet(String url) {
        try {
            URL httpUrl = new URL(url);
            HttpURLConnection connection = (HttpURLConnection) httpUrl.openConnection();
            connection.setRequestProperty("Content-Type", contentType);
            connection.setUseCaches(cache);
            connection.setInstanceFollowRedirects(true);

            connection.connect();
            logger.info("request [url: " + url + "]");

            BufferedReader res = new BufferedReader(new InputStreamReader(connection.getInputStream()));
            StringBuffer data = new StringBuffer();
            String line;
            while ((line = res.readLine()) != null) {
                data.append(line);
            }

            String resBody = data.toString();
            logger.info("response [body: " + resBody + "]");
            return resBody;
        } catch (IOException e) {
            e.printStackTrace();
        }
        logger.warning("request error");
        return "";
    }

    public static String sendPost(String url, String body) {
    	 try {
             URL httpUrl = new URL(url);
             HttpURLConnection connection = (HttpURLConnection) httpUrl.openConnection();

             connection.setRequestMethod(method);
             connection.setRequestProperty("Content-Type", contentType);
             connection.setUseCaches(cache);
             connection.setInstanceFollowRedirects(true);
             connection.setDoInput(true);
             connection.setDoOutput(true);
             logger.info("request [url: " + url + ", body: " + body + "]");
             connection.connect();
             // send req body
             OutputStreamWriter req = new OutputStreamWriter(connection.getOutputStream(), "UTF-8");
             req.write(body);
             req.flush();

             // get res body
             BufferedReader res = new BufferedReader(new InputStreamReader(connection.getInputStream()));
             StringBuffer data = new StringBuffer();
             String line;
             while ((line = res.readLine()) != null) {
                 data.append(line);
             }

             String resBody = data.toString();
             logger.info("response [body: " + resBody + "]");
             return resBody;
         } catch (MalformedURLException e) {
             e.printStackTrace();
         } catch (IOException e) {
             e.printStackTrace();
         }
         logger.warning("request error");
         return "";
     }
 }
