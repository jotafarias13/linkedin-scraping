#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""fetch_profile_data.py: minera as URLs de perfis e cria a tabela de usuários.

Utiliza as biblioteca BeatifulSoup e Selenium para encontrar os perfis
desejados e minera as URLs, criando a tabela de usuários.

"""


import time

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from utils import (
    DATABASE_PATH,
    LINKEDIN_URL,
    create_connection,
    create_driver,
    linkedin_login,
    populate_usuarios_table,
)

driver = create_driver()
driver = linkedin_login(driver)
time.sleep(1)

JOAO_PESSOA_URL = "https://www.linkedin.com/search\
/results/people/?geoUrn=%5B%22102858109%22%5D"
driver.get(JOAO_PESSOA_URL)

time.sleep(5)

profile_urls = []
PROFILE_INDICATOR = LINKEDIN_URL + "in/"

PROFILE_NUM = 1000

while True:
    content = driver.page_source
    soup = BeautifulSoup(content, "html.parser")

    a_class = soup.find_all(
        "a", {"class": "app-aware-link"}, href=True, target=False
    )
    hrefs = [a["href"] for a in a_class]

    href_profile = [
        href
        for href in hrefs
        if href.startswith(PROFILE_INDICATOR)
        and not href.startswith(PROFILE_INDICATOR + "AC")
    ]
    href_profile = list(set(href_profile))
    href_profile = [href.split("?")[0] for href in href_profile]

    profile_urls += href_profile

    if len(profile_urls) >= PROFILE_NUM:
        break

    next_page_button = driver.find_element(
        By.XPATH,
        "//span[text()='Avançar']",
    )
    next_page_button.click()
    time.sleep(4)

driver.quit()


db = create_connection(DATABASE_PATH)
populate_usuarios_table(db, profile_urls)
db.close()
