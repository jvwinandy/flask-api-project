import os
from abc import abstractmethod, ABC
from datetime import datetime
from typing import List

from sqlalchemy import create_engine, Engine, MetaData, text
import pandas as pd
from settings import DATABASE_PATH


class DataLoader(ABC):
    """ Loads data from a csv and stores in a database with 'table_name' and 'columns'. """
    def __init__(self, table_name: str, engine: Engine, columns: List[str] = None, usecols=None):
        self.table_name = table_name
        self.columns = columns
        self.usecols = usecols
        self.dataframes = []
        self.engine = engine
        self._script_dir = os.path.dirname(__file__)

    def load_folder(self, folder_path: str):
        """ Load data from multiple csvs in a directory. """
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".csv"):
                self.load_data(os.path.join(folder_path, file_name))

    def load_data(self, relative_file_path: str):
        """ Load data from a specific csv. """
        file_path = os.path.join(self._script_dir, relative_file_path)
        self.dataframes.append(pd.read_csv(file_path, names=self.columns, encoding="ISO-8859-1", header=1, sep=";",
                                           index_col="demanda_id", usecols=self.usecols))

    def apply_transformations(self):
        """ Apply custom transformations to the data. """
        for i in range(len(self.dataframes)):
            self.dataframes[i] = self._transformations(self.dataframes[i], i)

    def _transformations(self, data, idx):
        return data

    def insert_data_to_database(self):
        """ Insert the loaded data to the database table. """
        for data in self.dataframes:
            data.to_sql(self.table_name, con=engine, if_exists="append")
        engine.dispose()

    def create_table(self, drop_if_exists):
        """ Create a new database table. """
        metadata = MetaData()
        metadata.reflect(bind=engine)

        existing_table = metadata.tables.get(self.table_name)
        if existing_table is not None and drop_if_exists:
            existing_table.drop(bind=engine)

        with engine.connect() as connection:
            with open(f"{self._script_dir}/schema/{self.table_name.lower()}.sql", "r") as sql_schema_file:
                connection.execute(text(sql_schema_file.read()))
                connection.commit()


class DemandasLoader(DataLoader):
    """ Loader with special transformation specific to the demandas csv """
    def _transformations(self, data, idx):
        data = data.drop(columns=["competencia", "ultima_atualizacao"], axis=1)
        data['data_atendimento_demanda'] = data['data_atendimento_demanda'].map(self.convert_data_to_iso)
        return data

    @staticmethod
    def convert_data_to_iso(date_string):
        try:
            parsed_date = datetime.strptime(date_string, "%d/%m/%Y %H:%M:%S")
        except ValueError:
            # Some cells may not contain the time field.
            parsed_date = datetime.strptime(date_string, "%d/%m/%Y")
        return parsed_date.isoformat()


if __name__ == '__main__':
    engine = create_engine(DATABASE_PATH, echo=True)

    columns = ["ans", "razao_social", "beneficiarios", "demanda_id", "data_atendimento_demanda",
               "classificacao_demanda", "natureza_demanda", "subtema_demanda", "competencia", "ultima_atualizacao"]
    demandas_loader = DemandasLoader("Demandas", engine, columns)
    demandas_loader.create_table(True)
    demandas_loader.load_data("raw_data/dados-gerais-das-reclamacoes-por-operadora.csv")
    demandas_loader.apply_transformations()
    demandas_loader.insert_data_to_database()

    engine.dispose()