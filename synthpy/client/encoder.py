import json

from datetime import datetime, date, time
from decimal import Decimal


def json_serialize(*args, **kwargs):
    return json.dumps(*args, **kwargs, cls=Encoder)


class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%dT%H:%M:%S")
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        elif isinstance(obj, time):
            return obj.strftime("%H:%M:%S")
        elif isinstance(obj, Decimal):
            return float(obj)
        else:
            return json.JSONEncoder.default(self, obj)
