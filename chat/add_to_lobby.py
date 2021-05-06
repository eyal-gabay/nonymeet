import random
import string

from chat.security import remove_duplicate_agree


def found(user1: str, user2: str):
    a = []
    for line in open("database/lobby"):
        if line.split("username=")[1].split("&")[0] != user1:
            if line.split("username=")[1].split("&")[0] != user2:
                a.append(line)
    open("database/lobby", "w").close()
    for i in a:
        with open("database/lobby", "a") as database:
            database.write(i)


def find(username: str, gender: str, gender_i_want: str, age: int, min_age: int, max_age: int):
    file = open("database/agree")
    agree = file.read().splitlines()
    users_file = open("database/lobby")
    for user in users_file:
        he_is = False
        for m in agree:
            if username == m.split("`")[0] and user.split("username=")[1].split("&")[0] == m.split("`")[1]:
                he_is = True
                continue
        if not he_is:
            if user.split("username=")[1].split("&")[0] != username:
                if user.split("mygender=")[1].split("&")[0] == gender_i_want:
                    if user.split("genderiwant=")[1].split("&")[0] == gender:
                        if age >= int(user.split("minage=")[1].split("&")[0]) and age <= int(user.split("maxage=")[1].split("&")[0]):
                            print("here")
                            if int(user.split("myage=")[1].split("&")[0]) >= min_age and int(user.split("myage=")[1].split("&")[0]) <= max_age:
                                # found(user.split("username=")[1].split("&")[0], username)
                                users_file.close()
                                file.close()
                                return username + "." + user.split("username=")[1].split("&")[0]
        users_file.close()
        file.close()
        return False


def add(cookie: str, match: bool):
    remove_duplicate_agree()
    username = cookie.split(".")[0]
    database = open("database/profile")
    for user in database:
        if username == user.split("username=")[1].split("&")[0]:
            open("database/lobby", "a").write(user)
            e = find(user.split("username=")[1].split("&")[0], user.split("mygender=")[1].split("&")[0], user.split("genderiwant=")[1].split("&")[0], int(user.split("myage=")[1].split("&")[0]), int(user.split("minage=")[1].split("&")[0]), int(user.split("maxage=")[1].split("&")[0]))
            if e:
                ran = ["".join(random.choice(string.ascii_lowercase + "1234567890") for i in range(random.randrange(60, 70)))][0]
                if match:
                    print(e + " " + ran)
                database.close()
                return e + " " + ran
            else:
                database.close()
                return ""


def get_info(e: str):
    username = e.split()[0].split(".")[1]
    database = open("database/profile")
    for user in database:
        if username == user.split("username=")[1].split("&")[0]:
            database.close()
            return [username, user.split("mygender=")[1].split("&")[0], user.split("maxage=")[1].split("&")[0], user.split("aboutme=")[1]]


def two_agree(user: str, mate: str, agree: bool):
    database = open("database/agree", "a")
    database.write(f"{user}`{mate}`{agree}\n")
    database.close()
    check_if_two_agree(user, mate)


def check_if_two_agree(user: str, mate: str):
    database = open("database/agree")
    file = database.read().splitlines()
    file.reverse()
    a = False
    b = False
    for line in file:
        if user == line.split("`")[0] and mate == line.split("`")[1] and line.split("`")[2] == "True":
            a = True
        if user == line.split("`")[1] and mate == line.split("`")[0] and line.split("`")[2] == "True":
            b = True
        if a and b:
            read_file = open("database/chatpath", "a")
            read_file.write(f"{user}.{mate} " + ["".join(random.choice(string.ascii_lowercase + "1234567890") for i in range(random.randrange(60, 70)))][0] + "\n")
            read_file.close()
            break
    database.close()
