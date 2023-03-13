from utils import DATABASE_PATH, create_connection, execute_query

create_usuarios_table = """
CREATE TABLE IF NOT EXISTS usuarios (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  url TEXT NOT NULL
);
"""

create_linguas_table = """
CREATE TABLE IF NOT EXISTS linguas (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  id_pessoa INTEGER NOT NULL,
  lingua TEXT NOT NULL,
  nivel TEXT NOT NULL,
  FOREIGN KEY (id_pessoa) REFERENCES usuarios (id)
);
"""

create_competencias_table = """
CREATE TABLE IF NOT EXISTS competencias (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  id_pessoa INTEGER NOT NULL,
  competencia TEXT NOT NULL,
  FOREIGN KEY (id_pessoa) REFERENCES usuarios (id)
);
"""

create_interesses_table = """
CREATE TABLE IF NOT EXISTS interesses (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  id_pessoa INTEGER NOT NULL,
  interesse TEXT NOT NULL
  FOREIGN KEY (id_pessoa) REFERENCES usuarios (id)
);
"""

create_experiencias_table = """
CREATE TABLE IF NOT EXISTS experiencias (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  id_pessoa INTEGER NOT NULL,
  empresa INTEGER NOT NULL,
  data_comeco TEXT NOT NULL,
  data_fim TEXT NOT NULL,
  FOREIGN KEY (id_pessoa) REFERENCES usuarios (id)
);
"""


db = create_connection(DATABASE_PATH)

execute_query(db, create_usuarios_table)
execute_query(db, create_linguas_table)
execute_query(db, create_competencias_table)
execute_query(db, create_interesses_table)
execute_query(db, create_experiencias_table)

db.close()
