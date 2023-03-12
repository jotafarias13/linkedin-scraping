import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from config import LINKEDIN_LOGIN, LINKEDIN_PASSWORD

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

LINKEDIN_URL = "https://www.linkedin.com/"
driver.get(LINKEDIN_URL)

time.sleep(1)

username = driver.find_element(By.ID, "session_key")
username.send_keys(LINKEDIN_LOGIN)

password = driver.find_element(By.ID, "session_password")
password.send_keys(LINKEDIN_PASSWORD)

login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
login_button.click()

time.sleep(1)

JOAO_PESSOA_URL = "https://www.linkedin.com/search\
/results/people/?geoUrn=%5B%22102858109%22%5D"
driver.get(JOAO_PESSOA_URL)

# SEARCH_URL = "https://www.linkedin.com/search/results/people/"
# driver.get(SEARCH_URL)

# time.sleep(2)

# localidades_button = driver.find_element(
#     By.XPATH,
#     "//button[text()='Localidades']",
# )
# localidades_button.click()

# adicionar_localidade = driver.find_element(
#     By.XPATH,
#     "//*[@aria-label='Adicionar localidade']",
# )
# adicionar_localidade.send_keys("João Pessoa")

# clicar_localidade = driver.find_element(
#     By.XPATH,
#     "//span[text()='João Pessoa, Paraíba, Brasil']",
# )
# clicar_localidade.click()

# exibir_resultados = driver.find_element(
#     By.XPATH,
#     "//span[text()='Exibir resultados']",
# )
# exibir_resultados.click()

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

    profile_urls += href_profile

    if len(profile_urls) >= PROFILE_NUM:
        break

    next_page_button = driver.find_element(
        By.XPATH,
        # "//*[@aria-label='Avançar']/span",
        "//span[text()='Avançar']",
    )
    next_page_button.click()
    time.sleep(4)


driver.quit()

with open("profile_urls.txt", "w") as f:
    for prof in profile_urls:
        f.write(prof + "\n")
