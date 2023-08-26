import datetime
import json
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from flask_api.app import app
from flask_api.db import database
from flask_api.db.database import init_db, Base
from flask_api.db.models import Demanda
from flask_api.db.models.serializer import serialize


class TestDemandas(unittest.TestCase):
    DEMANDAS_BASE_ROUTE = "/demandas"

    def create_db(self):
        # in memory database for testing.
        mock_db_uri = "sqlite://"
        self.engine = create_engine(mock_db_uri)
        self.db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=self.engine))
        Base.query = self.db_session.query_property()

        database.engine = self.engine
        database.session = self.db_session

    def populate_db(self):
        for i in range(3):
            mock_demanda = Demanda(demanda_id=i,
                                   razao_social=f"company {i}",
                                   ans=i*2,
                                   beneficiarios=i*3,
                                   data_atendimento_demanda=datetime.datetime(2000+i, i+1, i+1, i, i, i),
                                   classificacao_demanda=f"classificacao {i}",
                                   natureza_demanda=f"natureza {i}",
                                   subtema_demanda=f"subtema {i}")
            self.mock_demandas.append(mock_demanda)
            self.db_session.add(mock_demanda)
        self.db_session.commit()

    def setUp(self):
        self.app = app.test_client()

        self.create_db()
        init_db()

        self.mock_demandas = []
        self.populate_db()

    def test_invalid_route(self):
        response = self.app.get("/notreallyavalidroute")
        self.assertEqual(404, response.status_code)

    def test_get_all_demandas(self):
        response = self.app.get(f"{self.DEMANDAS_BASE_ROUTE}")
        self.assertEqual(200, response.status_code)

        result_json = json.loads(response.data)
        self.assertEqual(3, len(result_json))
        self.assertEqual(serialize(self.mock_demandas), result_json)

    def test_get_demandas_ans_filter_exists_0(self):
        response = self.app.get(f"{self.DEMANDAS_BASE_ROUTE}?ans=0")
        self.assertEqual(200, response.status_code)

        result_json = json.loads(response.data)
        self.assertEqual(1, len(result_json))
        self.assertEqual(serialize(self.mock_demandas[0]), result_json[0])

    def test_get_demandas_ans_filter_exists_multiple(self):
        response = self.app.get(f"{self.DEMANDAS_BASE_ROUTE}?ans=0,2")
        self.assertEqual(200, response.status_code)

        result_json = json.loads(response.data)
        self.assertEqual(2, len(result_json))
        self.assertEqual(serialize(self.mock_demandas[:2]), result_json)

    def test_get_demandas_ans_filter_doesnt_exist(self):
        response = self.app.get(f"{self.DEMANDAS_BASE_ROUTE}?ans=1234")
        self.assertEqual(200, response.status_code)

        result_json = json.loads(response.data)
        self.assertEqual(0, len(result_json))

    def test_get_demandas_ans_classificacao_filters_exist(self):
        response = self.app.get(f"{self.DEMANDAS_BASE_ROUTE}?classificacao_demanda=classificacao%200&ans=0")
        self.assertEqual(200, response.status_code)

        result_json = json.loads(response.data)
        self.assertEqual(1, len(result_json))
        self.assertEqual([serialize(self.mock_demandas[0])], result_json)

    def test_get_demandas_ans_classificacao_filters_doesnt_exist(self):
        response = self.app.get(f"{self.DEMANDAS_BASE_ROUTE}?classificacao_demanda=classificacao%200&ans=123")
        self.assertEqual(200, response.status_code)

        result_json = json.loads(response.data)
        self.assertEqual(0, len(result_json))

    def test_demandas_count(self):
        response = self.app.get(f"{self.DEMANDAS_BASE_ROUTE}/count")
        self.assertEqual(200, response.status_code)

        result_json = json.loads(response.data)
        self.assertEqual(1, len(result_json))
        self.assertEqual({"total": 3}, result_json[0])

    def test_demandas_count_group_by_0(self):
        response = self.app.get(f"{self.DEMANDAS_BASE_ROUTE}/count?group_by=ans")
        self.assertEqual(200, response.status_code)

        result_json = json.loads(response.data)
        self.assertEqual(3, len(result_json))
        self.assertEqual([
            {"ans": 0, "total": 1},
            {"ans": 2, "total": 1},
            {"ans": 4, "total": 1}
        ], result_json)

    def test_demandas_count_filter(self):
        response = self.app.get(f"{self.DEMANDAS_BASE_ROUTE}/count?ans=4")
        self.assertEqual(200, response.status_code)

        result_json = json.loads(response.data)
        self.assertEqual(1, len(result_json))
        self.assertEqual({"total": 1}, result_json[0])

    def test_add_new_demanda_00(self):
        demanda_fields = {"ans": 12345, "razao_social": "test"}
        response = self.app.post(f"{self.DEMANDAS_BASE_ROUTE}/add", data=demanda_fields)
        self.assertEqual(201, response.status_code)

        # verify the creation
        response = self.app.get(f"{self.DEMANDAS_BASE_ROUTE}?ans=12345")
        self.assertEqual(200, response.status_code)

        result_json = json.loads(response.data)
        self.assertEqual(1, len(result_json))
        self.assertEqual({
            "ans": demanda_fields["ans"],
            'beneficiarios': None,
            'classificacao_demanda': None,
            'data_atendimento_demanda': None,
            'demanda_id': 3,
            'natureza_demanda': None,
            'razao_social': demanda_fields["razao_social"],
            'subtema_demanda': None
        }, result_json[0])

    def test_add_new_demanda_01(self):
        demanda_fields = {
            "ans": 67891,
            'beneficiarios': 15,
            'classificacao_demanda': "hard",
            'data_atendimento_demanda': "2049-12-01 01:23:45",
            'demanda_id': 3,
            'natureza_demanda': "artificial",
            'razao_social': "the company",
            'subtema_demanda': "just a test"
        }
        response = self.app.post(f"{self.DEMANDAS_BASE_ROUTE}/add", data=demanda_fields)
        self.assertEqual(201, response.status_code)

        # verify the creation
        response = self.app.get(f"{self.DEMANDAS_BASE_ROUTE}?ans=67891")
        self.assertEqual(200, response.status_code)

        result_json = json.loads(response.data)
        self.assertEqual(1, len(result_json))
        self.assertEqual(demanda_fields, result_json[0])

    def test_add_new_demanda_invalid_payload(self):
        response = self.app.post(f"{self.DEMANDAS_BASE_ROUTE}/add")
        self.assertEqual(400, response.status_code)

    def test_add_new_demanda_missing_not_null(self):
        demanda_fields = {
            'classificacao_demanda': "hard",
            'data_atendimento_demanda': "2049-12-01 01:23:45",
            'demanda_id': 3,
            'natureza_demanda': "artificial",
            'razao_social': "the company",
            'subtema_demanda': "just a test"
        }
        response = self.app.post(f"{self.DEMANDAS_BASE_ROUTE}/add", data=demanda_fields)
        self.assertEqual(400, response.status_code)
        self.assertEqual("Missing required field: ('ans',).", response.text)

    def test_add_new_demanda_missing_invalid_type(self):
        demanda_fields = {
            "ans": 67891,
            'beneficiarios': 15,
            'razao_social': "the company",
            'data_atendimento_demanda': "123",
        }
        response = self.app.post(f"{self.DEMANDAS_BASE_ROUTE}/add", data=demanda_fields)
        self.assertEqual(400, response.status_code)
        self.assertEqual("Invalid request: time data '123' does not match format '%Y-%m-%d %H:%M:%S'.", response.text)

    def test_update_demanda(self):
        demanda_fields = {
            "ans": 67891,
            'beneficiarios': 15,
            'razao_social': "the company"
        }

        response = self.app.put(f"{self.DEMANDAS_BASE_ROUTE}/update/0", data=demanda_fields)
        self.assertEqual(200, response.status_code)

        # verify the update
        response = self.app.get(f"{self.DEMANDAS_BASE_ROUTE}?demanda_id=0")
        self.assertEqual(200, response.status_code)

        result_json = json.loads(response.data)
        self.assertEqual(1, len(result_json))
        self.assertEqual({'ans': 67891,
                          'beneficiarios': 15,
                          'classificacao_demanda': 'classificacao 0',
                          'data_atendimento_demanda': '2000-01-01 00:00:00',
                          'demanda_id': 0,
                          'natureza_demanda': 'natureza 0',
                          'razao_social': 'the company',
                          'subtema_demanda': 'subtema 0'}, result_json[0])

    def test_update_demanda_doesnt_exist(self):
        demanda_fields = {
            "ans": 67891,
            'beneficiarios': 15,
            'razao_social': "the company"
        }

        response = self.app.put(f"{self.DEMANDAS_BASE_ROUTE}/update/14789632", data=demanda_fields)
        self.assertEqual(404, response.status_code)

    def test_update_demanda_invalid_date(self):
        demanda_fields = {
            'data_atendimento_demanda': "123"
        }

        response = self.app.put(f"{self.DEMANDAS_BASE_ROUTE}/update/0", data=demanda_fields)
        self.assertEqual(400, response.status_code)
        self.assertEqual("Invalid request: time data '123' does not match format '%Y-%m-%d %H:%M:%S'.", response.text)

    def test_demanda_delete(self):
        response = self.app.delete(f"{self.DEMANDAS_BASE_ROUTE}/delete/0")
        self.assertEqual(200, response.status_code)

        # getting the object should return empty.
        response = self.app.get(f"{self.DEMANDAS_BASE_ROUTE}?demanda_id=0")
        self.assertEqual(200, response.status_code)

        result_json = json.loads(response.data)
        self.assertEqual(0, len(result_json))

    def test_demanda_delete_doesnt_exist(self):
        response = self.app.delete(f"{self.DEMANDAS_BASE_ROUTE}/delete/1478932")
        self.assertEqual(404, response.status_code)


if __name__ == '__main__':
    unittest.main()
