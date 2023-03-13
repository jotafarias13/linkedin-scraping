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




## Outros
bib time não era necessária, tem como implementar pelo selenium mas faltou tempo.

Os imports para realizar a tarefa incluem o selenium e o webdriver_manager. Sendo compatível com Selenium 4, é necessário criar uma instância de service, não somente passar o PATH do executável do driver (por exemplo, chromedriver) como argumento para a função webdriver.Chrome. Foi escolhido o Chrome para realizar a tarefa. Na primeira execução, o código instala com driver.
