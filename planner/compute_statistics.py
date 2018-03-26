from datetime import date, timedelta

from planner import services, queries


def get_max_operations_date(operations, past_operations):
    """
    Iterate over the list of given operations and return the maximum due date

    :param operations: a list of operations
    :type operations: list

    :param past_operations: a list of past operations
    :type past_operations: list

    :return: the maximum due date
    :rtype: date
    """
    max_operation_date = None
    for operation in operations:
        operation_due_date = services.get_due_date(operation, past_operations)
        if max_operation_date is None or operation_due_date > max_operation_date:
            max_operation_date = operation_due_date
    return max_operation_date


def get_future_work_hours_by_week(garden_id):
    """ Compute the estimated number of hours to work by week on the garden with id garden_id """

    past_operations = queries.get_past_alerts(garden_id)
    future_operations = queries.get_future_alerts(garden_id)

    x_axis = {}
    y_axis = {}
    # Get production period. Its start date will be used as the first value of the X axis.
    production_start_date = services.get_current_production_period(garden_id).start_date
    # Get the production end date. It will be used as the last value of the X axis.
    production_end_date = get_max_operations_date(future_operations, past_operations)

    statistic_start_date = week_start_date(production_start_date.isocalendar()[0],
                                           production_start_date.isocalendar()[1])
    statistic_end_date = week_start_date(production_end_date.isocalendar()[0],
                                         production_end_date.isocalendar()[1])

    x_axis = get_mondays_of_weeks_between_two_dates(statistic_start_date, statistic_end_date)
    y_axis = dict.fromkeys(x_axis.keys(), 0.0)

    for fop in future_operations:
        op_week = services.get_due_date(fop, past_operations).isocalendar()[1]
        y_axis[op_week] += from_timedelta_to_hours(services.get_expected_duration(fop))
    return x_axis, y_axis


def get_mondays_of_weeks_between_two_dates(start_date, end_date):
    mondays_of_weeks = {}
    current_statistic_date = start_date
    while current_statistic_date <= end_date:
        week_number = current_statistic_date.isocalendar()[1]
        mondays_of_weeks[week_number] = current_statistic_date
        current_statistic_date = current_statistic_date + timedelta(days=7)
    return mondays_of_weeks


def from_timedelta_to_hours(interval_time):
    """
    Convert timedelta from Python to hours

    :param interval_time: TimeDelta
    :return: the interval in hours
    """
    return interval_time.total_seconds() / 3600


def week_start_date(year, week):
    d = date(year, 1, 1)
    delta_days = d.isoweekday() - 1
    delta_weeks = week
    if year == d.isocalendar()[0]:
        delta_weeks -= 1
    delta = timedelta(days=-delta_days, weeks=delta_weeks)
    return d + delta
