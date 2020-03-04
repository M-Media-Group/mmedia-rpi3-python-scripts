from . import generateReport
from ..memail import memail
from .. import config
from datetime import date
import os

congrats_thresholds = [
    10000, 9000, 8000, 7000, 6000, 5000, 4000, 3000, 2000, 1000, 500, 250
]
follower_count = int(
    generateReport.dates_dict[generateReport.last_day]['followers'])
report_path = generateReport.workspace_path + '/logs/sentCongrats.txt'
os.makedirs(os.path.dirname(report_path), exist_ok=True)


def congratulate():
    congrats_nahh = []
    f = open(generateReport.workspace_path + "/logs/sentCongrats.txt", "a+")
    today = str(date.today())
    f.seek(0)
    for row in f:
        # Split the row columns (space delimited)
        a, b = row.split()
        congrats_nahh = [int(b)]

    for congrats in congrats_thresholds:
        if congrats not in congrats_nahh and (congrats <= follower_count <=
                                              congrats + 150):
            subject = "Congratulations on " + str(
                "{:,}".format(congrats)) + " followers!"
            body = "Hi!\n\nIt's your Instagram Bot checking in! I just wanted to congratulate you on reaching " + str(
                "{:,}".format(congrats)) + " followers! Congratulations :)!"
            print("Congratulations on " + str("{:,}".format(congrats)) +
                  " followers!")
            memail.sendEmail(subject, body, config.settings['client']['email'])
            f.write(today + " " + str(congrats) + '\n')
            break
