from datetime import date, timedelta

from planner import services, queries


def get_work_hours_by_week(garden_id):
    """ Compute the estimated number of hours to work by week on the garden with id garden_id """
    past_operations = queries.get_past_alerts(garden_id)
    future_operations = queries.get_future_alerts(garden_id)
    weeks = {}
    for fop in future_operations:
        op_week = services.get_due_date(fop, past_operations).isocalendar()[1]
        if not weeks.get(str(op_week)):
            weeks[str(op_week)] = 0.0
        weeks[str(op_week)] += from_timedelta_to_hours(services.get_expected_duration(fop))
    print(weeks)
    return weeks


def from_timedelta_to_hours(interval_time):
    """ Convert timedelta from Python to hours """
    return interval_time.total_seconds()/3600
