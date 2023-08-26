import datetime

from sqlalchemy import inspect, Row


def serialize(rows):
    if isinstance(rows, Serializer):
        # serialize using attributes.
        return type(rows).serialize_obj(rows)
    elif len(rows) == 1 and isinstance(rows[0], Serializer):
        # if we only have one element we dont need to create another list.
        return serialize(rows[0])
    elif isinstance(rows, Row):
        return rows._asdict()
    elif isinstance(rows, Row):
        # uses sqlalchemy row dict method for serialization.
        return rows._asdict()
    else:
        # last case, it's a list, serialize it as one.
        return [serialize(obj) for obj in rows]


class Serializer(object):
    def serialize_obj(self):
        result = {}
        for key in inspect(self).attrs.keys():
            result[key] = getattr(self, key)
            if isinstance(result[key], datetime.datetime):
                # Datetime is not serializable.
                result[key] = str(result[key])
        return result

