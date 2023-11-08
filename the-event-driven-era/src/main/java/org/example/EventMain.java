package org.example;
import java.sql.SQLException;
import java.util.Scanner;
import java.util.UUID;

/*
 * Class interacts directly with the command-line,
 * holds functions that call validator and SQLite functions.
 */
public class EventMain {


    private static Insert ins = new Insert();

    private static int option;

    public static void main(String[] args) {

        System.out.println("\033[1;38;5;225mGreetings!\nWelcome to the ARCHITECT'S Monolithic Event Planning Application\033[0m");
        Scanner scanner = new Scanner(System.in);
        String option;

        // until the user quits
        do {
            // continually prompt for VALID action
            do {
                System.out.println(
                        """
                                \033[1;38;5;225mEnter the number associated with the action you'd like to complete:\033[0m
                                \033[38;5;15m1 Insert
                                2 View
                                3 Quit\033[0m""");
                option = scanner.nextLine();
            } while (!Validator.isValidOption(option));

            System.out.println("\033[1;38;5;225mYou picked option " + option + ".\033[0m");

            EventMain.option = Integer.parseInt(option);
            // switch based on
            switch (EventMain.option) {
                case 1:
                    insert(scanner);
                    break;
                case 2:
                    view(scanner);
                    break;
                case 3:
                    System.out.println("\033[1;38;5;225mSee you later!!!\033[0m");
                    break;
            }
        } while (EventMain.option != 3);
    }

    /* CLI sequence for insertion */
    private static void insert(Scanner scanner) {
        // figure out which table
        Character table = tablePrompt(scanner);
        if (table == 'A')
            newEvent(scanner);
        else
            newParticipant(scanner);
    }

    /* CLI sequence for viewing */
    private static void view(Scanner scanner) {
        // figure out which table
        Character table = tablePrompt(scanner);
        if (table == 'A')
            viewEvents();
        else
            viewParticipants();

    }

    private static void newEvent(Scanner scanner) {

        System.out.println("\033[1;38;5;75mYou've selected to insert into the Events table.");
        System.out.println("Let's create a new Event!\033[0m");

        // UUID INPUT
        String uuid = "";
        boolean status = false;
        boolean generate = false;

        do {
            System.out.println("\033[38;5;33mInsert UUID [Optional: To generate, enter VOID]");
            uuid = scanner.nextLine();

            if (uuid.equals("VOID")) {
                generate = true;
            }
            // save the result of the check
            if (!generate) {
                status = Validator.validateUUID(uuid);
            }

            // if VOID : generate UUID
            if (generate) {
                // if randomUUID already exists in DB, generate new one
                while (!status) {
                    uuid = UUID.randomUUID().toString();
                    status = Validator.validateUUID(uuid);
                }
                System.out.println("Generated UUID: " + uuid);
            }

        } while (!status);

        // DATE INPUT
        String date = "";
        do {
            System.out.println("Insert Event Date [YYYY-MM-DD]");
            date = scanner.nextLine();
        } while (!Validator.isValidDate(date));

        // TIME INPUT
        String time = "";
        do {
            System.out.println("Insert Event Time [HH:MM AM/PM]");
            time = scanner.nextLine();
        } while (!Validator.isValidTime(time));

        // TITLE INPUT
        String title = "";
        do {
            System.out.println("Insert Event Title [Max. 255]");
            title = scanner.nextLine();
        } while (!Validator.isValidTitle(title));

        // DESCRIPTION INPUT
        String description = "";
        do {
            System.out.println("Insert Event Description [Max. 600]");
            description = scanner.nextLine();
        } while (!Validator.isValidDescription(description));

        // EMAIL INPUT
        String email = "";
        do {
            System.out.println("Insert Event Host's Email\033[0m");
            email = scanner.nextLine();
        } while (!Validator.isValidEmail(email));

        int statusCode = ins.insertEvent(uuid, date, time, title, description, email);
        System.out.println(statusCode);
    }

    private static void newParticipant(Scanner scanner) {
        System.out.println("\033[1;38;5;225mYou've selected to insert into the Registered table.");
        System.out.println("Let's register a participant!\033[0m");

        // PARTICIPANT UUID INPUT
        String participant_uuid = "";
        boolean status = false;
        boolean generate = false;

        do {
            System.out.println("\033[38;5;105mInsert Participant UUID [Optional: To generate, enter VOID]");
            participant_uuid = scanner.nextLine();

            if (participant_uuid.equals("VOID")) {
                generate = true;
            }
            // save the result of the check
            if (!generate) {
                status = Validator.validateUUID(participant_uuid);
            }

            // if VOID : generate UUID
            if (generate) {
                // if randomUUID already exists in DB
                while (!status) {
                    participant_uuid = UUID.randomUUID().toString();
                    status = Validator.validateUUID(participant_uuid);
                }
                System.out.println("Generated Participant UUID: " + participant_uuid);
            }

        } while (!status);

        // EVENT UUID INPUT
        String event_UUID = "";
        do {
            System.out.println("Insert Event ID [UUID]");
            event_UUID = scanner.nextLine();
        } while (!Validator.validateUUID(event_UUID));

        // NAME INPUT
        String name = "";
        do {
            System.out.println("Insert Participant Name");
            name = scanner.nextLine();
        } while (!Validator.isValidName(name));

        // EMAIL INPUT
        String email = "";
        do {
            System.out.println("Insert Participant Email");
            email = scanner.nextLine();
        } while (!Validator.isValidEmail(email));

        int statusCode = ins.insertParticipant(participant_uuid, event_UUID, name, email);
        System.out.println(statusCode);
    }

    /* CLI sequence for determining table */
    private static Character tablePrompt(Scanner scanner) {
        String table = "";
        // continually prompt for VALID table selection
        do {
            System.out.println(
                    "\033[1;38;5;225mPick a table you'd like to access. Enter the letter associated with the table you'd like to access:\033[0m");
            System.out.println("\033[38;5;15mA Events\nB Registered\033[0m");
            table = scanner.nextLine();
        } while (!Validator.isValidTable(table));

        return Character.toUpperCase(table.charAt(0));
    }

    /* Adds an event in Events table */


    /* Validates entry and creates a participant in Participants table */


    /* Returns a table of participants currently registered */
    public static void viewEvents() {
        System.out.println("\033[1;91;38;5;196m" + ins.getEventEndpoint() + "\033[0m");
    }

    /* Returns a table of participants currently registered */
    public static void viewParticipants() {
        System.out.println("\033[1;91;38;5;196m" + ins.getPartEndpoint() + "\033[0m");
    }
}