from flask import request


def create_filtered_query(query, model):
    for column, values in request.args.items():
        if column == 'group_by':
            continue

        column_obj = getattr(model, column)
        if column_obj is not None:
            query = query.filter(column_obj.in_(values.split(',')))
    return query


def create_group_by_query(query, columns):
    for column_obj in columns:
        query = query.group_by(column_obj)
    return query