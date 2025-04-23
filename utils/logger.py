import datetime

def log(message):
    with open("grokbot.log", "a") as f:
        f.write(f"{datetime.datetime.now()} - {message}\n")