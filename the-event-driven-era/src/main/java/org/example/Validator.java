package org.example;

import java.util.regex.Pattern;

/*
 * Class validates user inputs,
 * holds functions that will pre-check fields before accessing the DB
 */
public class Validator {



    public static boolean validateUUID(String uuid) {
        Pattern pattern = Pattern.compile("^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}$");
        return pattern.matcher(uuid).matches();
    }

    public static boolean isValidDate(String date){
        if (date.length() > 10 || !date.matches("[\\d-]+")){
            return false;
        }
        String[] dateValues = date.split("-");
        if  (dateValues.length != 3){
            return false;
        }
        int year = Integer.parseInt(dateValues[0]);
        int month = Integer.parseInt(dateValues[1]);
        int day = Integer.parseInt(dateValues[2]);
        return year > 0 && year <= 9999 && month >= 1 && month <= 12 && day >= 1 && day <= 31;
    }

    public static boolean isValidTime(String time){
        String[] extractTime = time.split(" ");
        if (extractTime.length != 2 || !(extractTime[1].equals("AM") || extractTime[1].equals("PM"))){
            return false;
        }
        String[] hoursMinutes = extractTime[0].split(":");
        if (hoursMinutes.length != 2 || hoursMinutes[1].length() != 2) return false;
        int hour = Integer.parseInt(hoursMinutes[0]);
        int minutes = Integer.parseInt(hoursMinutes[1]);
        return hour > 0 && hour <= 12 && minutes >= 0 && minutes <= 59;
    }

    public static boolean isValidTitle(String eventTitle){
        return eventTitle.length() <= 255;
    }

    public static boolean isValidDescription(String eventDescription){
        return eventDescription.length() <= 600;
    }

    public static boolean isValidEmail(String hostEmail){
        String EMAIL_PATTERN = "^(?=.{1,64}@)[A-Za-z0-9_-]+(\\.[A-Za-z0-9_-]+)*@"
                + "[^-][A-Za-z0-9-]+(\\.[A-Za-z0-9-]+)*(\\.[A-Za-z]{2,})$";
        Pattern pattern = Pattern.compile(EMAIL_PATTERN);
        return pattern.matcher(hostEmail).matches();
    }

    public static boolean isValidName(String name){
        return name.length() <= 600 && name.length() != 0;
    }


    /* check for valid input (table) */
    public static boolean isValidTable(String s){
        // if not one character
        if (s.length() != 1)
            return false;

        // return if user inputted A or B
        return Character.toUpperCase(s.charAt(0)) == 'A' || Character.toUpperCase(s.charAt(0)) == 'B';
    }

    /* check for valid input (option) */
    public static boolean isValidOption(String s){
        // if not one character
        if (s.length() != 1)
            return false;

        // if not a digit
        if (!Character.isDigit(s.charAt(0)))
            return false;

        // if not a digit in bounds (will never be negative)
        if (Integer.parseInt(s) > 3) {
            System.out.println("INVALID OPTION");
            return false;
        }

        return true;
    }
}
