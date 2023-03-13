# Raspagem de Dados LinkedIn
Esse projeto tem como objetivo realizar a raspagem de dados do LinkedIn para fomentar análises sobre as informações de seus usuários. Em geral, o projeto consiste em procurar perfis de pessoas da região de João Pessoa, Paraíba, Brasil e minerar dados pertinentes de seus perfis. Na mineração, foram obtidos dados de idiomas, competências, interesses (empresas) e experiências. Esses dados foram armazenados em um banco de dados *sqlite3*, com cada tabela se relacionando através de uma ID de usuário (perfil). Ao final, foram gerados alguns gráficos que possibilitam analisar com mais profundidade os dados minerados.


## Dependências
As bibliotecas necessárias para executar esse projeto são:

- [sqlite3](https://docs.python.org/3/library/sqlite3.html) (nativa de python)
- [time](https://docs.python.org/3/library/time.html) (nativa de python)
- [bs4](https://beautiful-soup-4.readthedocs.io/en/latest/) (BeautifulSoup)
- [selenium](https://selenium-python.readthedocs.io/)
- [webdriver_manager](https://github.com/SergeyPirogov/webdriver_manager)
- [matplotlib](https://matplotlib.org/stable/index.html)
- [pandas](https://pandas.pydata.org/docs/)

A biblioteca *sqlite3* foi utilizada para comunicação com o banco de dados, desde sua criação até sua manipulação. A biblioteca *selenium* em conjunto com *webdriver_manager* foram utilizadas para conseguir acesso ao perfil do LinkedIn e navegar pelas páginas, fazendo pesquisas e minerando os dados. O *webdriver_manager* possibilita a instalação de um driver de browser (neste projeto foi utilizado o Chrome) para que a *selenium* consiga navegar. A biblioteca *time* foi usada nesse mesmo contexto, visto que é necessário esperar um tempo até que a página carregue por completo para que o HTML seja baixado por completo. A própria biblioteca *selenium* tem essa [funcionalidade](https://www.selenium.dev/documentation/webdriver/waits/), porém, não houve tempo hábil para que isso fosse implementado da maneira mais adequada e a biblioteca *time* foi escolhida para que o tempo fosse investido em outras partes do projeto. Por fim, as bibliotecas *matplotlib* e *pandas* foram usadas para gerar os gráficos que resumem os dados minerados neste projeto.


## Utilização

Para reproduzir este projeto em seu computador, é necessário seguir alguns passos.

1. Criar um arquivo `config.py` com as variáveis `LINKEDIN_LOGIN` e `LINKEDIN_PASSWORD` para que esses dados fiquem protegidos de serem acessado por outras pessoas.

```
LINKEDIN_LOGIN = "login"
LINKEDIN_PASSWORD = "senha"
```

2. Instalar o requirements do projeto. Para isso, é recomendado criar um ambiente virtual e instalar os pacotes nele. Vale salientar que **versão de python** utilizada nesse projeto foi a 3.11.1.

```
pip install -r requirements.txt
```





