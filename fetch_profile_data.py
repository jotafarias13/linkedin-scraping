import time

from utils import (
    DATABASE_PATH,
    create_connection,
    create_driver,
    execute_query_return,
    get_competencias_from_usuario,
    get_experiencias_from_usuario,
    get_id_usuario,
    get_idiomas_from_usuario,
    get_interesses_from_usuario,
    insert_competencia,
    insert_experiencia,
    insert_idioma,
    insert_interesses,
    linkedin_login,
)

db = create_connection(DATABASE_PATH)
select_usarios = """
SELECT url FROM usuarios
"""
usuarios_url = execute_query_return(db, select_usarios)
db.close()

usuarios_url = [user_url[0] for user_url in usuarios_url]
usuarios_idioma = [pu + "/details/languages" for pu in usuarios_url]
usuarios_competencia = [pu + "/details/skills" for pu in usuarios_url]
usuarios_interesse = [pu + "/details/interests" for pu in usuarios_url]
usuarios_experiencia = [pu + "/details/experience" for pu in usuarios_url]


driver = create_driver()
driver = linkedin_login(driver)
time.sleep(1)

db = create_connection(DATABASE_PATH)

# for user_url, user_idioma, user_comp, user_inter, user_exp in zip(usuarios_url, usuarios_idioma, usuarios_competencia, usuarios_interesse, usuarios_experiencia):
TOTAL = 100
for user_url, user_idioma, user_comp, user_inter, user_exp in zip(
    usuarios_url[:TOTAL],
    usuarios_idioma[:TOTAL],
    usuarios_competencia[:TOTAL],
    usuarios_interesse[:TOTAL],
    usuarios_experiencia[:TOTAL],
):
    id_usuario = get_id_usuario(db, user_url)

    driver.get(user_idioma)
    time.sleep(2)
    content = driver.page_source
    langs_names_levels = get_idiomas_from_usuario(content)
    if langs_names_levels is not None:
        insert_idioma(db, langs_names_levels, id_usuario)

    driver.get(user_comp)
    time.sleep(2)
    content = driver.page_source
    competencias = get_competencias_from_usuario(content)
    if competencias is not None:
        insert_competencia(db, competencias, id_usuario)

    driver.get(user_inter)
    time.sleep(2)
    content = driver.page_source
    interesses = get_interesses_from_usuario(content)
    if interesses is not None:
        insert_interesses(db, interesses, id_usuario)

    driver.get(user_exp)
    time.sleep(2)
    content = driver.page_source
    experiencias = get_experiencias_from_usuario(content)
    if experiencias is not None:
        insert_experiencia(db, experiencias, id_usuario)

driver.quit()
db.close()
