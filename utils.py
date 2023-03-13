import sqlite3
import time
from sqlite3 import Error

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from config import LINKEDIN_LOGIN, LINKEDIN_PASSWORD

DATABASE_PATH = "linkedin_scraping.sqlite3"


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


def execute_query_return(
    connection: sqlite3.Connection, query: str
) -> list[tuple]:
    cursor = connection.cursor()
    result = None

    try:
        cursor.execute(query)
        result = cursor.fetchall()
    except Error as e:
        print(f"Erro: {e}")

    return result


def populate_usuarios_table(
    connection: sqlite3.Connection, profile_urls: list
) -> None:
    for pu in profile_urls:
        insert_usuario = f"""
        INSERT INTO
        usuarios (url)
        VALUES
        ('{pu}');
        """
        execute_query(connection, insert_usuario)


def create_driver() -> webdriver.Chrome:
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    return driver


LINKEDIN_URL = "https://www.linkedin.com/"


def linkedin_login(driver: webdriver.Chrome) -> webdriver.Chrome:
    driver.get(LINKEDIN_URL)

    time.sleep(1)

    username = driver.find_element(By.ID, "session_key")
    username.send_keys(LINKEDIN_LOGIN)

    password = driver.find_element(By.ID, "session_password")
    password.send_keys(LINKEDIN_PASSWORD)

    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()

    return driver


NO_CONTENT = "Nada para ver por enquanto"


def get_id_usuario(connection: sqlite3.Connection, user_url: str) -> int:
    select_usuario_id = f"""
    SELECT id
    FROM usuarios
    WHERE url = '{user_url}'
    """
    id_usuario = execute_query_return(connection, select_usuario_id)[0][0]

    return id_usuario


def get_idiomas_from_usuario(content: str) -> dict[str, str]:
    if NO_CONTENT in content:
        return None

    soup = BeautifulSoup(content, "html.parser")
    langs_table = soup.find("ul", {"class": "pvs-list"})
    langs = langs_table.find_all("span", {"aria-hidden": "true"})
    langs_names = [l.text for idx, l in enumerate(langs) if idx % 2 == 0]
    langs_levels = [l.text for idx, l in enumerate(langs) if idx % 2 == 1]

    langs_names_levels = {
        key: value
        for key, value in zip(langs_names, langs_levels)
        if value.startswith("Nível") or value.startswith("Fluente")
    }

    return langs_names_levels


def insert_idioma(
    connection: sqlite3.Connection,
    langs_names_levels: dict[str, str],
    id_usuario: int,
) -> None:
    for name, level in langs_names_levels.items():
        insert_idioma = f"""
        INSERT INTO
        linguas (id_pessoa, lingua, nivel)
        VALUES
        ({id_usuario}, '{name}', '{level}');
        """
        execute_query(connection, insert_idioma)

    return None


def get_competencias_from_usuario(content: str) -> list[str]:
    if NO_CONTENT in content:
        return None

    soup = BeautifulSoup(content, "html.parser")
    comps_table = soup.find("ul", {"class": "pvs-list"})
    comps_bold = comps_table.find_all("span", {"class": "t-bold"})

    competencias = []
    for comp in comps_bold:
        comp_text = comp.find("span", {"aria-hidden": "true"}).text
        competencias.append(comp_text)

    return competencias


def insert_competencia(
    connection: sqlite3.Connection,
    competencias: list[str],
    id_usuario: int,
) -> None:
    for comp in competencias:
        insert_competencia = f"""
        INSERT INTO
        competencias (id_pessoa, competencia)
        VALUES
        ({id_usuario}, '{comp}');
        """
        execute_query(connection, insert_competencia)

    return None


def get_interesses_from_usuario(content: str) -> list[str]:
    if NO_CONTENT in content:
        return None

    soup = BeautifulSoup(content, "html.parser")
    if "Top Voices" in content:
        soup = soup.find("div", hidden=True)
    inter_table = soup.find("ul", {"class": "pvs-list"})
    inter_bold = inter_table.find_all("span", {"class": "t-bold"})

    interesses = []
    for inter in inter_bold:
        inter_text = inter.find("span", {"aria-hidden": "true"}).text
        interesses.append(inter_text)

    return interesses


def insert_interesses(
    connection: sqlite3.Connection,
    interesses: list[str],
    id_usuario: int,
) -> None:
    for inter in interesses:
        insert_interesse = f"""
        INSERT INTO
        interesses (id_pessoa, interesse)
        VALUES
        ({id_usuario}, '{inter}');
        """
        execute_query(connection, insert_interesse)

    return None


def convert_str_data(data: str) -> tuple[str, str]:
    mes = {
        "jan": "01",
        "fev": "02",
        "mar": "03",
        "abr": "04",
        "mai": "05",
        "jun": "05",
        "jul": "07",
        "ago": "08",
        "set": "09",
        "out": "10",
        "nov": "11",
        "dez": "12",
    }

    data_range = data.split("·")[0]
    begin = data_range.split("-")[0].strip()
    end = data_range.split("-")[1].strip()

    begin_ano = begin[-4:]
    if begin.startswith("1") or begin.startswith("2"):
        begin_mes = "01"
    else:
        begin_mes = mes[begin[:3]]
    begin_dia = "01"
    begin_clean = begin_ano + "-" + begin_mes + "-" + begin_dia

    if end == "o momento":
        end_clean = "atualmente"
    else:
        end_ano = end[-4:]
        if end.startswith("1") or end.startswith("2"):
            end_mes = "01"
        else:
            end_mes = mes[end[:3]]
        end_dia = "01"
        end_clean = end_ano + "-" + end_mes + "-" + end_dia

    return begin_clean, end_clean


def get_experiencias_from_usuario(content: str) -> dict[str, tuple]:
    if NO_CONTENT in content:
        return None

    soup = BeautifulSoup(content, "html.parser")
    exps_table = soup.find("ul", {"class": "pvs-list"})
    exps_entity = exps_table.find_all("div", {"class": "pvs-entity"})

    cargos = []
    datas = []
    for exp_ent in exps_entity:
        exp_bold = exp_ent.find("span", {"class": "t-bold"})
        exp_text = exp_bold.find("span", {"aria-hidden": "true"}).text
        cargos.append([exp_text])

        exp_light = exp_ent.find("span", {"class": "t-black--light"})
        exp_text = exp_light.find("span", {"aria-hidden": "true"}).text
        datas.append([exp_text])

    cargo_data = {cargo[0]: data[0] for cargo, data in zip(cargos, datas)}

    for cargo, data in cargo_data.items():
        if "-" not in data:
            return None
        cargo_data[cargo] = convert_str_data(data)

    return cargo_data


def insert_experiencia(
    connection: sqlite3.Connection,
    experiencias: dict[str, tuple],
    id_usuario: int,
) -> None:
    for cargo, data in experiencias.items():
        insert_experiencia = f"""
        INSERT INTO
        experiencias (id_pessoa, empresa, data_comeco, data_fim)
        VALUES
        ({id_usuario}, '{cargo}', '{data[0]}', '{data[1]}');
        """
        execute_query(connection, insert_experiencia)

    return None
