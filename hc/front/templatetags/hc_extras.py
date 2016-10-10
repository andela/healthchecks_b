from django import template

register = template.Library()


class Unit(object):
    def __init__(self, name, nsecs):
        self.name = name
        self.plural = name + "s"
        self.nsecs = nsecs

MINUTE = Unit("minute", 60)
HOUR = Unit("hour", MINUTE.nsecs * 60)
DAY = Unit("day", HOUR.nsecs * 24)
WEEK = Unit("week", DAY.nsecs * 7)


@register.filter
def hc_duration(td):
    remaining_seconds = int(td.total_seconds())
    result = []

    for unit in (WEEK, DAY, HOUR, MINUTE):
        if unit == WEEK and remaining_seconds % unit.nsecs != 0:
            # Say "8 days" instead of "1 week 1 day"
            continue

        v, remaining_seconds = divmod(remaining_seconds, unit.nsecs)
        if v == 1:
            result.append("1 %s" % unit.name)
        elif v > 1:
            result.append("%d %s" % (v, unit.plural))

    return " ".join(result)


@register.filter
def convert(td):
    """Return the tuple of days, hours, minutes and seconds."""

    seconds = int(td.total_seconds())
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)
    months, weeks = divmod(weeks, 4)
    years, months = divmod(months, 12)

    output = str(years) + ' year(s) ' if years > 0 else ''
    output += str(months) + ' month(s) ' if months > 0 else ''
    output += str(weeks) + ' week(s) ' if weeks > 0 else ''
    output += str(days) + ' day(s) ' if days > 0 else ''
    output += str(hours) + ' hour(s) ' if hours > 0 else ''
    output += str(minutes) + ' min(s)' if minutes > 0 else ''
    # return years, months, weeks, days, hours, minutes, seconds
    return output
