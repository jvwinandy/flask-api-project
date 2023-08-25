import json
from datetime import datetime

from flask import Flask, jsonify, request, Response
from sqlalchemy import select, func, inspect

from flask_api.db.models import Demanda
import flask_api.db.database as db
from flask_api.db.models.serializer import serialize

app = Flask(__name__)
db.init_db()


def create_filtered_query(query, model):
    for column, values in request.args.items():
        if column == 'group_by':
            continue

        column_obj = getattr(model, column)
        if column_obj is not None:
            query = query.filter(column_obj.in_(values.split(',')))
    return query


def create_group_by_query(query, model, columns):
    for column_obj in columns:
        query = query.group_by(column_obj)
    return query


@app.route('/')
def hello_world():  # put application's code here
    r = db.session.execute(select(Demanda).where(Demanda.ans == 43)).first()
    return serialize(r)


@app.route('/demandas')
def demandas():
    """ Returns all Demandas sorted by id. This query can be filtered with '?filter_column=value' """
    query = select(Demanda)
    query = create_filtered_query(query, Demanda)

    result = db.session.execute(query).all()

    return serialize(result)


@app.route('/demandas/count')
def demandas_count():
    """
    Returns the count of all demandas. The query can also specify grouping with '?group_by=column(s)' and be filtered.
    """
    group_columns = request.args.get("group_by")
    group_columns = group_columns.split(',') if group_columns is not None else []
    select_columns = [func.count(Demanda.demanda_id).label("total")]
    for column in group_columns:
        column_obj = getattr(Demanda, column)
        if column_obj is not None:
            select_columns.append(column_obj)

    query = select(*select_columns)
    query = create_group_by_query(query, Demanda, select_columns[1:])
    query = create_filtered_query(query, Demanda)

    result = db.session.execute(query).all()
    return serialize(result)


@app.route('/demandas/add', methods=['POST'])
def demandas_create_new():
    """ Add a new demanda with an auto generated id. """
    data = request.form
    try:
        data_atendimento_demanda = data.get("data_atendimento_demanda")
        if data_atendimento_demanda is not None:
            data_atendimento_demanda = datetime.strptime(data_atendimento_demanda, "%Y-%m-%d %H:%M:%S")
        new_demanda = Demanda(ans=data['ans'],
                              razao_social=data['razao_social'],
                              beneficiarios=data.get("beneficiarios"),
                              data_atendimento_demanda=data_atendimento_demanda,
                              classificacao_demanda=data.get("classificacao_demanda"),
                              natureza_demanda=data.get("natureza_demanda"),
                              subtema_demanda=data.get("subtema_demanda"))
        db.session.add(new_demanda)
    except KeyError as e:
        return Response(f"Missing required field: {e.args}.", status=400)
    except Exception as e:
        return Response(f"Invalid request: {e}.", status=400)

    db.session.commit()
    return "Item created successfully."


@app.route('/demandas/update/<int:demanda_id>', methods=['PUT'])
def demandas_update(demanda_id):
    """ Update a Demanda with 'id'. """
    data = request.form

    query = select(Demanda).where(Demanda.demanda_id == demanda_id)
    demanda_to_update = db.session.execute(query).first()[0]
    if not demanda_to_update:
        return Response(f"Couldn't find object with id: {id}", status=404)

    for key in inspect(demanda_to_update).attrs.keys():
        new_value = data.get(key)
        if new_value is not None:
            if key == 'data_atendimento_demanda':
                new_value = datetime.strptime(new_value, "%Y-%m-%d %H:%M:%S")
            setattr(demanda_to_update, key, new_value)
    db.session.commit()
    return "Item updated successfully."


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()


if __name__ == '__main__':
    app.run()
