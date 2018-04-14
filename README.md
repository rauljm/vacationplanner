Crie uma pasta chamada vacationplanner dentro do seu diretório de projetos (mkdir vacationplanner).

Crie um virtualenv com python 3 chamado vacationplanner. Eu usei o virtualenv wrapper. Caso não teha configurado, siga esse tutorial: http://www.arruda.blog.br/programacao/python/usando-virtualenvwrapper/.

Dentro do virtualenv, rode o comando `pip install -r requirements.txt` para instalar as depedências do projeto.

Antes de mais nada, precisamos criar uma base de simulação que irá conter os dias de um ano e seus respectivos climas para cada cidade (São Paulo, Rio de Janeiro, Porto Alegre e Pernambuco), para tal, siga as seguintes instruções:

No seu terminal no diretório vacationplanner:
`PYTHONPATH=planner iptyhon3`
`from planner.utils import create_json_file_with_random_conditions_climate`
`create_json_file_with_random_conditions_climate(ANO_DESEJADO)`

Para inicar a aplicação, dentro do diretório vacationplanner:
`PYTHONPATH=planner python planner/app/app.py`
E acesse a URL: `http://127.0.0.1:5000/`

Para rodar os testes da aplicação, dentro do diretório vacationplanner:
`PYTHONPATH=planner nosetests planner/test/models.py planner/test/controller.py planner/test/app.py`
