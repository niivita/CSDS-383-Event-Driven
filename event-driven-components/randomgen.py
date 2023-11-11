import random
import calendar
import names
import uuid


def random_time():
    hour = random.randint(0, 12)
    minute = random.randint(0, 59)
    time_of_day = random.choice(['AM', 'PM'])
    time = "{:02d}:{:02d} {}".format(hour, minute, time_of_day)
    return time


def random_date():
    month = random.randint(1, 12)
    max_days = calendar.monthrange(2023, month)[1]
    day = random.randint(1, max_days)
    date = "{:02d}-{:02d}".format(month, day)
    return date


def random_event_desc():
    event_types = ["Conference", "Computer Science Event", "Music Festival", "Career fair", "Art Exhibition"]
    locations = ["southside of Cleveland", "at Case", "in Leutner", "on the second floor of library",
                 "at the bottom of Tomlinson"]
    participants = ["attended by international students", "with the alumni of case",
                    "with leaders from various industries",
                    "for art enthusiasts", "with international performers"]
    additional_details = ["featuring live music", "along delicious food and drinks", "showcasing past achievements",
                          "and food will be served", "and the CEO of *company* will be showing"]

    event_type = random.choice(event_types)
    location = random.choice(locations)
    participant_detail = random.choice(participants)
    additional_detail = random.choice(additional_details)

    title = f"{event_type}"

    # Generate description
    description = f"{event_type} {location} {participant_detail} {additional_detail}."

    return title, description


def random_event():
    event_dict = {}
    event_id = str(uuid.uuid4())
    name = names.get_full_name()
    email = name.replace(" ", "").lower() + "@gmail.com"
    title, desc = random_event_desc()
    event_dict["eventID"] = event_id
    event_dict["date"] = random_date()
    event_dict["time"] = random_time()
    event_dict["title"] = title
    event_dict["description"] = desc
    event_dict["email"] = email
    return event_dict


def random_participant(event_id):
    part_dict = {}
    part_dict["participantID"] = str(uuid.uuid4())
    part_dict["eventID"] = str(event_id)
    name = names.get_full_name()
    email = name.replace(" ", "").lower() + "@gmail.com"
    part_dict["name"] = name
    part_dict["email"] = email

    return part_dict