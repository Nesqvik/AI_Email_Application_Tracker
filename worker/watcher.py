import time
import calendar
from datetime import datetime
from core.report import send_report


def is_last_day_of_month():
    today = datetime.now()

    last_day = calendar.monthrange(
        today.year,
        today.month
    )[1]

    return today.day == last_day

def start_worker():

    report_sent = False

    while True:

        print("Checking emails...")
        
        if should_send_report() and not report_sent:
            send_report()
            report_sent = True

        if datetime.now().day != calendar.monthrange(
            datetime.now().year,
            datetime.now().month
        )[1]:
            report_sent = False

        time.sleep(120)

def should_send_report():
    now = datetime.now()

    last_day = calendar.monthrange(now.year, now.month)[1]

    return (
        now.day == last_day
        and now.hour == 18
        and now.minute < 2
    )

if __name__ == "__main__":
    start_worker()