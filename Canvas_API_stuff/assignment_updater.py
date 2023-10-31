# Author: Peter Rock
# Last Edit: 31 Oct 2023

# This is a little python script that is designed to make changing the due dates
# on lots of assignments within a coordinated course easier. In order to 
# run this script from either PowerShell or from the zsh (MacOS) or bash (Linux)
# terminal, you will need to make sure that Python is installed. The latest version
# of Python can be found at https://www.python.org/downloads/ and once python is 
# installed, you will likely need to run the following command from the terminal:
# pip install requests pytz
# However, after that, you will be ready to run the script. Once you have made the 
# necessary modifications to this file, just open the terminal (or PowerShell)
# to this folder and run the command 
# python assignment_updater.py
# and it will do the rest :)

import requests
from datetime import datetime
import pytz


BASE_URL = "https://canvas.colorado.edu/api/v1"

# You will need to generate your own API token 
# This can be found in the Account -> Settings -> Approved Integrations
# TOKEN = "You Thought!"
TOKEN = "10772~pTpmDkVzzMWzO8siailONiH3X4ypZRcKIDKmeyJETyAWzhlTxRl45TrEf02oUeFE"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}"
}


# You can get the course id from the URL. In this case, the URL for the course 
# is given by https://canvas.colorado.edu/courses/95894
course_id = "20901"


# Set the time for each of the sections of the semester
# the time format for this NEEDS to be YYYY-MM-DDTHH:MM:SS
# so 2 pm on August 31, 2023 would be "2023-08-31T14:00:00"
time_dict = {
    "001" : "08:00",
    "002" : "09:05",
    "003" : "10:10",
    "004" : "14:30",
}


sections = requests.get(f"{BASE_URL}/courses/{course_id}/sections?per_page=100", headers=HEADERS).json()

# Just grab these from the URL
# I got these from the end of https://canvas.colorado.edu/courses/95894/assignments/1731552
# The ones that are provided here are for Hw1-Hw15
# General heuristic is that the unlock date is Wednesday the week before
# Assignment_id, Unlock_date, Due_date
assignment_info = [
    (1837126, "2023-11-22", "2023-11-30"),
    (1837127, "2023-11-29", "2023-11-07"),
    (1837128, "2023-12-06", "2023-12-14"),
    (1837129, "2023-12-13", "2023-12-21")
]


# =================================================
# The following part should not need to be changed!
# =================================================


# Needed since all times in the Canvas CLI are given in UTC
def mt_to_utc(mt_time_str):
    # Define the time format and time zones
    format = "%Y-%m-%dT%H:%M:%S"
    mountain = pytz.timezone('America/Denver')
    utc = pytz.utc

    # Parse the provided Mountain Time date-time string
    naive_datetime = datetime.strptime(mt_time_str, format)
    localized_datetime = mountain.localize(naive_datetime)

    # Convert to UTC
    utc_datetime = localized_datetime.astimezone(utc)
    
    # The return here is hacky, but will work so long as we don't have any classes
    # that start after 6 pm
    return utc_datetime.strftime(format)


# Now we can actually update the assignments
for (assignment_id, unlock_day, due_day) in assignment_info:
    
    print(f"The assignment id is {assignment_id}")

    for section_name in time_dict.keys():
        # find section id
        section_id = None
        for section in sections:
            if section['name'] == section_name:
                section_id = section['id']
                break 

        if not section_id:
            print(section_name, "Not Found")
            exit()


        overrides = requests.get(f"{BASE_URL}/courses/{course_id}/assignments/{assignment_id}/overrides", headers=HEADERS).json()
        
        override_id = None
        for override in overrides:
            if override.get('course_section_id') == section_id:
                override_id = override['id']
                break


        new_unlock_day = mt_to_utc(unlock_day + "T" + time_dict[section_name] + ":00") + "Z"
        new_due_date = mt_to_utc(due_day + "T" + time_dict[section_name] + ":00") + "Z"


        if override_id:  # If an override exists, update it
            data = {
                "assignment_override[unlock_at]": new_unlock_day,
                "assignment_override[due_at]": new_due_date,
                "assignment_override[lock_at]": new_due_date,
            }
            # put method is for updating
            requests.put(f"{BASE_URL}/courses/{course_id}/assignments/{assignment_id}/overrides/{override_id}", headers=HEADERS, data=data)
        else:  # If no override exists, create a new one for section 007
            data = {
                "assignment_override[course_section_id]": section_id,
                "assignment_override[unlock_at]": new_unlock_day,
                "assignment_override[due_at]": new_due_date,
                "assignment_override[lock_at]": new_due_date
            }
            # post method for new items
            requests.post(f"{BASE_URL}/courses/{course_id}/assignments/{assignment_id}/overrides", headers=HEADERS, data=data)

        print(f"\tDue date updated successfully for {section_name}!", end = "\r")
    print("                                                                             ", end = "\r")
    
print("Finished updating all assignments!")