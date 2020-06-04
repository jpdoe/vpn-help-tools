#! /usr/bin/python

# Generate TODO list for certificates renew
# Author: Jan Polák

import re

from datetime import datetime


class User:
    def __init__(self, name, state, region, city, company, email, expir):
        self.name = name.strip()
        self.state = state.strip()
        self.region = region.strip()
        self.city = city.strip()
        self.company = company.strip()
        self.email = email.strip()
        self.expir = datetime.strptime(expir.strip(), "%b %d %H:%M:%S %Y")
        self.crt = ""
        self.ovpn = ""

    def read_date_time(self):
        return self.expir.strftime("%d.%m.%Y %H:%M")

    def read_date(self):
        return self.expir.strftime("%d. %m. %Y")

    def read_record(self):
        return [
            self.name,
            self.state,
            self.region,
            self.city,
            self.company,
            self.email,
            self.read_date_time(),
        ]


# regex for searching - [\s\r]* is for match any white-space incl. \r (Win)
regex = re.compile(
    r"[\s\r]*C=(?P<state>.*?)[\s\r]*,[\s\r]*ST=(?P<region>.*?)[\s\r]*,[\s\r]*L=(?P<city>.*?)[\s\r]*,[\s\r]*O=(?P<company>.*?)/emailAddress=(?P<email>.*?)[\s\r]*,[\s\r]*CN=(?P<user_name>.*?)[\s\r]*,[\s\r]*Not[\s\r]*After[\s\r]:[\s\r](?P<expir>[\s\S]*)"
)

# Return content of input file
def get_users(INPUT_FILE):
    file = open(INPUT_FILE, "r")
    file_cont = file.read()
    file.close()

    users = file_cont.split("GMT")
    return users


# Write to file with formatting
def write_users(list_of_users, OUTPUT_FILE):
    file = open(OUTPUT_FILE, "w+", encoding="utf-8")

    for user in list_of_users:
        items = user.read_record()
        for item in items:
            file.write(item + "\n")
        file.write("-" * 10 + "\n")
    file.close()


# Parse list of users with regexp
def parse_users(list_of_users):
    users = []
    for item in list_of_users:
        match = regex.search(item)
        # match = regex.match(item)
        if match:
            new_user = User(
                match.group("user_name"),
                match.group("state"),
                match.group("region"),
                match.group("city"),
                match.group("company"),
                match.group("email"),
                match.group("expir"),
            )
            users.append(new_user)
    return users


# create and write asnwers(w/wo question) for each user
def make_write_answer(list_of_users):
    for user in list_of_users:
        answer_file = open("answers\\" + user.name + ".txt", "w", encoding="utf-8")

        answer_file.write(f"{user.email}\n")
        answer_file.write(
            f"Obnova certifikátu pro {user.company} \n\n"
        )  # print email and company

        answer_file.write(f"dne {user.read_date()} Vám vyprší platnost certifikátu.")

        answer_file.write("\n\n")

        answer_file.close()


if __name__ == "__main__":
    INPUT_FILE = "example_input.txt "
    now = datetime.now()
    OUTPUT_FILE = "TODO_list_" + now.strftime("D%d_%m-T%H-%M") + ".txt"
    users = get_users(INPUT_FILE)
    list_of_users = parse_users(users)
    write_users(list_of_users, OUTPUT_FILE)
    make_write_answer(list_of_users)
