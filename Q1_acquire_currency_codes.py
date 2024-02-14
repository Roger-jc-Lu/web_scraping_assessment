from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import itertools

webdriver_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=webdriver_service)

url = "https://www.11meigui.com/tools/currency"
driver.get(url)
driver.implicitly_wait(5)

target = driver.find_element(By.ID, "desc")
continents = target.find_elements(By.TAG_NAME, "tbody")
entries = [i.find_elements(By.TAG_NAME, "tr")[2:] for i in continents]
entries = list(itertools.chain.from_iterable(entries))
entries = [i.find_elements(By.TAG_NAME, "td") for i in entries]
entries = [(i[4].text, i[1].text) for i in entries]
entries = list(set(entries))

driver.quit()

file_path = 'currency_codes.txt'

with open(file_path, 'w') as file:
    for entry in entries:
        file.write(f"{entry[0]}:{entry[1]}\n")


