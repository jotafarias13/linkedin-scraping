import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from config import LINKEDIN_LOGIN, LINKEDIN_PASSWORD

profile_urls = []
with open("profile_urls.txt", "r") as file:
    for f in file:
        profile_urls.append(f)


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

driver.get(profile_urls[0])
content = driver.page_source

with open("profile1.html", "w") as file:
    file.write(content)
