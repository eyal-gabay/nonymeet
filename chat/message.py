def add(username, massage):
    open("database/message/send_message", "a").write(f"{username}`{massage}")


def read(username, _remove=False):
    database = open("database/message/send_message")
    for line in database:
        # print(username, line.strip().split("`")[0])
        if username == line.strip().split("`")[0]:
            database.close()
            if _remove:
                remove(line)
            return [line.strip().split("`")]
    database.close()
    return None


def remove(line):
    a = []
    with open("database/message/send_message") as database:
        for i in database:
            if i.strip() != line.strip():
                a.append(i.strip())
    open("database/message/send_message", "w").close()
    for i in a:
        with open("database/message/send_message", "a") as database:
            database.write(i.strip() + "\n")

