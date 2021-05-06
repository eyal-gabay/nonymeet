def likes_page(user: str):
    a = []
    for line in open("database/chatpath"):
        users = line.split()[0].split(".")
        if user in users:
            a.append(line.strip())
    return a


def names(matches: list, user: str):
    a = []
    for match in matches:
        for username in match.split()[0].split("."):
            if username != user:
                a.append(username)
    return a


def room_name(user, chat_user):
    for line in open("database/chatpath"):
        if user in line.split(" ")[0].split(".") and chat_user in line.split(" ")[0].split("."):
            return line.split()[1]


def take_text(user, path):
    text = []
    date = []
    send_from = []
    try:
        for line in open("database/chat_rooms/" + path):
            text.append(line.split("`")[0])
            date.append(line.split("`")[1])
            send_from.append(line.split("`")[2].strip() == user)
        return list(zip(text, date, send_from))   # , send_from]
    except FileNotFoundError:
        return ""
    except TypeError:
        return "error"


def last_msg(user: str, users: list):
    path = []
    a = []
    for i in users:
        path.append(room_name(user, i))
    for user in range(len(users)):
        try:
            a.append(take_text(users[user], path[user])[-1][0])
            # users[user] + "`" +
        except IndexError:
            pass
    return a
