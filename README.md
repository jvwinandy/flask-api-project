API REST feita em Python3, usando flask e SQLAlchemy para trabalhar com dados de uma tabela de demandas (reclamações)
de empresas de saúde, contendo todos as operações CRUD

Para baixar os dados é necessário usar **git lfs pull**, ou baixar os dados csv no link: 
https://dadosabertos.ans.gov.br/FTP/PDA/IGR/dados-gerais-das-reclamacoes/ e inserir na pasta raw_data.

Fonte dos dados: https://dados.gov.br/dados/conjuntos-dados/indice-geral-de-reclamacoes---igr-metodologia-ate-2022 - Dados gerais das Reclamações

## How to Build And Run
### Build:
docker-compose build flask-api
### Run:
#### Create db:
docker-compose run --rm flask-api python db_utility/data_loader.py
#### Run API:
docker-compose run --rm flask-api flask run --host=0.0.0.0

## Visão geral da estrutura do projeto:

src/db_utility: Arquivos para criação do banco de dados e inserção dos dados no mesmo.

src/db_utility/data_loader.py: Ferramenta para inserção dos dados do csv para o banco de dados.

src/db_utility/schema/demandas.sql: Definição do schema da tabela Demandas.

--

src/flask_api: API para acesso e manipulação dos dados criados no banco de dados.

src/flask_api/db/models/demanda.py: Definição do modelo da tabela demandas

src/flask_api/db/models/serializer.py: Classe base para facilitar a serialização dos dados retornados pelo SQLAlchemy.

src/flask_api/db/database.py: Módulo que inicializa a engine e session do banco de dados.

src/flask_api/routes/demadas.py: Rotas principais da aplicação. Aplica o CRUD na tabela de Demandas.

src/flask_api/tests/test_demandas.py: Testes para as rotas /demandas/

src/flask_api/utils.py: Funções de utilidade para a API.

src/flask_api/app.py: Roda o aplicativo Flask.

## Rotas:
(Arquivo de testes contém exemplos das execuções.)

GET: /demandas: Retorna todas as demandas, pode ser filtrada com "?column=value"

GET: /demandas_count: Retorna o total de demandas, pode ser filtrada e agrupada usando "?group_by=column"

POST: /demandas/add: Adiciona uma nova demanda. Dados devem ser enviados usando form-data.

PUT: /demandas/update/<int:demanda_id>: Atualiza uma demanda com novos valores (enviados usando form-data)

DELETE: /demandas/delete/<int:demanda_id>: Deleta demanda com demanda_id.