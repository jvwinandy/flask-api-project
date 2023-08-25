import unittest

from db_utility.data_loader import DataLoader


class TestDataLoader(unittest.TestCase):
    def test_load_operadoras_data(self):
        columns = ["ans", "razao_social", "beneficiarios", "demanda", "data_atendimento_demanda",
                   "classificacao_demanda", "natureza_demanda", "subtema_demanda", "competencia", "ultima_atualizacao"]
        loader = DataLoader("Operadoras", columns)
        loader.load_data("../raw_data/dados-gerais-das-reclamacoes-por-operadora.csv")


if __name__ == '__main__':
    unittest.main()
