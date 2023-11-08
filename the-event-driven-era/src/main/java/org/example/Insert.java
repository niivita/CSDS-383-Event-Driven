package org.example;

import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.utils.URIBuilder;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.ObjectWriter;



public class Insert {

    private static String eventEndpoint = "https://t6r6u8jln4.execute-api.us-east-1.amazonaws.com/main/events/";

    private static String partEndpoint = "https://t6r6u8jln4.execute-api.us-east-1.amazonaws.com/main/participants/";

    static ObjectMapper mapper = new ObjectMapper();

    public int insertEvent(String eventID, String date, String time, String title, String description, String email) {

        try {

            URIBuilder uriBuilder = new URIBuilder(eventEndpoint)
                    .addParameter("eventID", eventID)
                    .addParameter("date", date)
                    .addParameter("time", time)
                    .addParameter("title", title)
                    .addParameter("description", description)
                    .addParameter("email", email);

            HttpPost request = new HttpPost(uriBuilder.build());

            try (CloseableHttpClient client = HttpClients.createDefault();
                 CloseableHttpResponse response = client.execute(request)) {


                return response.getStatusLine().getStatusCode();
            }


        } catch (Exception e) {
            e.printStackTrace();
            return -1;
        }
    }

    public int insertParticipant(String participantID, String eventID, String name, String email) {

        try {

            URIBuilder uriBuilder = new URIBuilder(partEndpoint)
                    .addParameter("participantID", participantID)
                    .addParameter("eventID", eventID)
                    .addParameter("name", name)
                    .addParameter("email", email);

            HttpPost request = new HttpPost(uriBuilder.build());


            try (CloseableHttpClient client = HttpClients.createDefault();
                 CloseableHttpResponse response = client.execute(request)) {

                return response.getStatusLine().getStatusCode();
            }

        } catch (Exception e) {
            e.printStackTrace();
            return -1;
        }
    }

    public String getEventEndpoint(){
        return getEndpoint(eventEndpoint);
    }

    public String getPartEndpoint(){
        return getEndpoint(partEndpoint);
    }

    private static String getEndpoint(String apiEndpoint) {
        try{

            HttpGet httpGet = new HttpGet(apiEndpoint);

            try (CloseableHttpClient client = HttpClients.createDefault();
                 CloseableHttpResponse response = client.execute(httpGet)) {

                System.out.println("Event Status Code: " + response.getStatusLine().getStatusCode());

                return prettyPrintJson(EntityUtils.toString(response.getEntity()));
            }

        } catch (Exception e){
            e.printStackTrace();
            return null;
        }

    }

    public static String prettyPrintJson(String jsonString) {
        try {
            // Create an ObjectMapper
            ObjectMapper objectMapper = new ObjectMapper();

            ObjectWriter objectWriter = objectMapper.writerWithDefaultPrettyPrinter();

            Object json = objectMapper.readValue(jsonString, Object.class);
            return objectWriter.writeValueAsString(json);
        } catch (JsonProcessingException e) {
            e.printStackTrace();
            return null;
        }
    }

    public static void main(String[] args){

        int statusCode;
        //String body = getEventEndpoint();
        //statusCode = insertEvent("Test8", "Test8Date", "Time8", "Title8", "Desc8", "chase@gmail");
        //statusCode = insertParticipant("Part8", "Test8", "Chase8", "chase@gmail.com");

        //System.out.println(statusCode)
        System.out.println("\033[52;38;5;213mThis text is red\033[0m");

    }

}
