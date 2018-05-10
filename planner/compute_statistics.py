from datetime import date, timedelta
import collections

from planner import services, queries
from planner.models import Operation


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
    max_operation_date = date.today()
    for operation in operations:
        operation_due_date = services.get_due_date(operation, past_operations)
        if max_operation_date is None or operation_due_date > max_operation_date:
            max_operation_date = operation_due_date
    return max_operation_date


def get_min_operations_date(future_operations, past_operations):
    """
    Iterate over the list of given operations and return the minimum due date

    :param operations: a list of operations
    :type operations: list

    :param past_operations: a list of past operations
    :type past_operations: list

    :return: the maximum due date
    :rtype: date
    """
    min_operation_date = date.today()
    for operation in future_operations:
        operation_due_date = services.get_due_date(operation, past_operations)
        if min_operation_date is None or operation_due_date < min_operation_date:
            min_operation_date = operation_due_date
    for operation in past_operations:
        operation_due_date = Operation.objects.get(original_alert=operation).execution_date
        if min_operation_date is None or operation_due_date < min_operation_date:
            min_operation_date = operation_due_date
    return min_operation_date


def get_min_history_operations_date(history_operations):
    """
    Iterate over the list of Operation and return the smallest execution_date
    """
    min_operation_date = None
    for operation in history_operations:
        if min_operation_date is None or operation.execution_date < min_operation_date:
            min_operation_date = operation.execution_date
    return min_operation_date


def get_max_history_operations_date(history_operations):
    """
    Iterate over the list of Operation and return the maximum execution_date
    """
    max_operation_date = None
    for operation in history_operations:
        if max_operation_date is None or operation.execution_date > max_operation_date:
            max_operation_date = operation.execution_date
    return max_operation_date


def get_statistics_start_end_dates_for_productions_date(production_start_date,
                                                        production_end_date):
    statistic_start_date = week_start_date(production_start_date.isocalendar()[0],
                                           production_start_date.isocalendar()[1])
    statistic_end_date = week_start_date(production_end_date.isocalendar()[0],
                                         production_end_date.isocalendar()[1])
    return statistic_start_date, statistic_end_date


def build_statistics_axis_per_week_for_productions_date(production_start_date,
                                                        production_end_date):
    statistic_start_date, statistic_end_date = get_statistics_start_end_dates_for_productions_date(
        production_start_date=production_start_date,
        production_end_date=production_end_date)
    x_axis = get_mondays_of_weeks_between_two_dates(statistic_start_date, statistic_end_date)
    y_axis = dict.fromkeys(x_axis.keys(), 0.0)

    return x_axis, y_axis


def get_future_work_hours_by_week(garden_id):
    """ Compute the estimated number of hours to work by week on the garden with id garden_id """

    past_operations = queries.get_past_alerts(garden_id)
    future_operations = queries.get_future_alerts(garden_id)

    x_axis = {}
    y_axis = {}
    # Get production period. Its start date will be used as the first value of the X axis.
    production_start_date = get_min_operations_date(future_operations, past_operations)
    # Get the production end date. It will be used as the last value of the X axis.
    production_end_date = get_max_operations_date(future_operations, past_operations)

    x_axis, y_axis = build_statistics_axis_per_week_for_productions_date(production_start_date=production_start_date,
                                                                         production_end_date=production_end_date)

    for fop in future_operations:
        op_week = services.get_due_date(fop, past_operations).isocalendar()[1]
        y_axis[op_week] += from_timedelta_to_hours(services.get_expected_duration(fop))
    return x_axis, y_axis


def get_actual_work_hours_by_week(garden_id):
    """ Compute the number of hours of work done by week on the garden with id garden_id """

    history = services.get_current_history(garden_id=garden_id)
    history_operations = services.get_history_operations(history_id=history.id)

    production_start_date = get_min_history_operations_date(history_operations)
    production_end_date = get_max_history_operations_date(history_operations)

    if production_start_date is None or production_end_date is None:
        raise NoHistoryError()

    x_axis, y_axis = build_statistics_axis_per_week_for_productions_date(production_start_date=production_start_date,
                                                                         production_end_date=production_end_date)
    for history_operation in history_operations:
        if history_operation.duration is not None and history_operation.execution_date is not None:
            op_week = history_operation.execution_date.isocalendar()[1]
            y_axis[op_week] += from_timedelta_to_hours(history_operation.duration)

    return x_axis, y_axis


def fill_missing_values_between_two_dict(dict1, dict2, default_value=None):
    """
    Compare the keys of the two given dictionaries and add the missing keys so
    that they both have the same keys.
    The missing keys are associated to the given default_value if provided.
    If no default_value is provided, it uses the value from the dictionary
    that has the key and copy it into the dictionary that misses the key.
    """

    for key_dict1 in dict1.keys():
        if key_dict1 not in dict2:
            dict2[key_dict1] = default_value if default_value is not None else dict1[key_dict1]
    for key_dict2 in dict2.keys():
        if key_dict2 not in dict1:
            dict1[key_dict2] = default_value if default_value is not None else dict2[key_dict2]
    return dict1, dict2


def get_estimated_and_actual_work_hours_per_week(garden_id):
    # Compute both statistics
    x_axis_estimated, y_axis_estimated = get_future_work_hours_by_week(garden_id)
    x_axis_actual, y_axis_actual = get_actual_work_hours_by_week(garden_id)
    # Make sure the dictionaries have the sames keys
    x_axis_estimated, x_axis_actual = fill_missing_values_between_two_dict(x_axis_estimated, x_axis_actual)
    y_axis_estimated, y_axis_actual = fill_missing_values_between_two_dict(y_axis_estimated, y_axis_actual, 0.0)
    # Order the dictionaries by key (=week numbers) because in the HTML template, we won't use the keys
    x_axis_estimated = collections.OrderedDict(sorted(x_axis_estimated.items()))
    x_axis_actual = collections.OrderedDict(sorted(x_axis_actual.items()))
    y_axis_estimated = collections.OrderedDict(sorted(y_axis_estimated.items()))
    y_axis_actual = collections.OrderedDict(sorted(y_axis_actual.items()))
    return x_axis_estimated, y_axis_estimated, x_axis_actual, y_axis_actual


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
    """
    Get the first Monday of the given week for teh given year.
    https://stackoverflow.com/a/1287862/2179668
    """
    d = date(year, 1, 1)
    delta_days = d.isoweekday() - 1
    delta_weeks = week
    if year == d.isocalendar()[0]:
        delta_weeks -= 1
    delta = timedelta(days=-delta_days, weeks=delta_weeks)
    return d + delta


class NoHistoryError(Exception):
    pass
