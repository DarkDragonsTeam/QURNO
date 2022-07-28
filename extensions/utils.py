from . import *
from .date import jalali

from django.utils import timezone

# Create your custom utils and abilities here. (Pure Python and Pure technics)


def get_jalali_date(time):
    # First we get a complete list of the Jalali/Hijri Solar months.
    jalali_months = [
        "فروردین",
        "اردیبهشت",
        "خرداد",
        "تیر",
        "مرداد",
        "شهریور",
        "مهر",
        "آبان",
        "آذر",
        "دی",
        "بهمن",
        "اسفند",
    ]

    # Contrary to what you may think, the time sent to us by Django is not the time of Asia/Tehran, and it becomes a
    # Gregorian date. Here we retrieve our local time (same Asia / Tehran) from timezone module.
    time = timezone.localtime(time)

    # The jalali module we received requires a variable in string format and a specific behavior.
    # Here we build this method for our module, then pass it to the module and get the result.
    time_to_str = "{} {} {}".format(time.year, time.month, time.day)
    time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()

    # The result of this module is a tuple, something that Python cannot change (or manipulate).
    # We convert it to a list and store it in a new variable so that we can make the desired changes to them.
    time_to_list = list(time_to_tuple)

    # The result of this module is a tuple, something that Python cannot change (or manipulate). We convert it to a
    # list and store it in a new variable so that we can make the desired changes to them.
    for index, month in enumerate(jalali_months):
        if time_to_list[1] == index + 1:
            time_to_list[1] = month
            break

    # Now it's time to design the whole result in the form of a variable in a specific format and finally return it.
    output = "{} {} {} - ساعت {} و {} دقیقه".format(
        time_to_list[2],
        time_to_list[1],
        time_to_list[0],
        time.hour,
        time.minute,
    )

    return str(output)


def get_jalali_today(time=timezone.now()):
    jalali_months = [
        "فروردین",
        "اردیبهشت",
        "خرداد",
        "تیر",
        "مرداد",
        "شهریور",
        "مهر",
        "آبان",
        "آذر",
        "دی",
        "بهمن",
        "اسفند",
    ]

    time = timezone.localtime(time)

    time_to_str = "{} {} {}".format(time.year, time.month, time.day)
    time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()

    time_to_list = list(time_to_tuple)

    for index, month in enumerate(jalali_months):
        if time_to_list[1] == index + 1:
            time_to_list[1] = month
            break
        
    output = "{} {} {}".format(
        time_to_list[2],
        time_to_list[1],
        time_to_list[0],
    )

    return str(output)
