import sqlite3
from sqlite3 import Error


def create_connection(path_to_file: str) -> sqlite3.Connection:
    connection = None

    try:
        connection = sqlite3.connect(path_to_file)
        print(f"Conexão com o banco {path_to_file} foi realizada")
    except Error as e:
        print(f"Erro: {e}")

    return connection


def execute_query(connection: sqlite3.Connection, query: str) -> None:
    cursor = connection.cursor()

    try:
        cursor.execute(query)
        connection.commit()
    except Error as e:
        print(f"Erro: {e}")


create_linguas_table = """
CREATE TABLE IF NOT EXISTS linguas (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  id_pessoa INTEGER NOT NULL,
  lingua TEXT NOT NULL,
  nivel TEXT NOT NULL
);
"""

create_competencias_table = """
CREATE TABLE IF NOT EXISTS competencias (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  id_pessoa INTEGER NOT NULL,
  competencia TEXT NOT NULL
);
"""

create_empresas_table = """
CREATE TABLE IF NOT EXISTS empresas (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  empresa TEXT NOT NULL
);
"""

create_experiencias_table = """
CREATE TABLE IF NOT EXISTS experiencias (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  id_pessoa INTEGER NOT NULL,
  id_empresa INTEGER NOT NULL,
  data_comeco TEXT NOT NULL,
  data_fim TEXT NOT NULL
);
"""


db = create_connection("linkedin_scraping.sqlite3")

execute_query(db, create_linguas_table)
execute_query(db, create_competencias_table)
execute_query(db, create_empresas_table)
execute_query(db, create_experiencias_table)
