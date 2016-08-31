try:
    import simplejson as json
except ImportError:
    import json


def time_dict_to_seconds(value):
    if value is None:
        return None
    if isinstance(value, str):
        time_conf = json.loads(value)
    elif isinstance(value, dict):
        time_conf = value
    else:
        raise ValueError('Invalid type %s' % type(value))
    days_to_seconds = time_conf.get('days', 0) * 24 * 60 * 60
    hours_to_seconds = time_conf.get('hours', 0) * 60 * 60
    minutes_to_seconds = time_conf.get('minutes', 0) * 60
    return days_to_seconds + hours_to_seconds + minutes_to_seconds + time_conf.get('seconds', 0)
