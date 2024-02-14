from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.select import Select
from datetime import datetime
try:
    import argparse
except ImportError:
    print("argparse is not installed")


parser = argparse.ArgumentParser(description="get most recent selling rate for a currency on a specific date from Bank of China.")
parser.add_argument('date', type=str, help="The selected date, in the form of YYYYMMDD")
parser.add_argument('currency', type=str, help="The target currency, in iso-4217 currency codes")
args = parser.parse_args()

# Convert date to the format required by the website
date = datetime.strptime(args.date, '%Y%m%d')
date = date.strftime('%Y-%m-%d')

# initialization
webdriver_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=webdriver_service)

url = "https://www.boc.cn/sourcedb/whpj/enindex2.htm"
driver.get(url)
driver.implicitly_wait(5)

# param input
driver.switch_to.frame("DataList")
target = driver.find_element(By.NAME, "historysearchform")
start_date = target.find_element(By.NAME, "erectDate")
start_date.clear()
start_date.send_keys(date)

end_date = target.find_element(By.NAME, "nothing")  
end_date.clear()
end_date.send_keys(date)  

currency_dropdown = Select(target.find_element(By.NAME, "pjname"))

# Exception handling
try:
    currency_dropdown.select_by_value(args.currency)
    search_button = driver.find_element(By.XPATH, '//input[@value="search"]')
    search_button.click()

    table = driver.find_elements(By.TAG_NAME, 'tbody')[2]
    entry = table.find_elements(By.TAG_NAME, 'tr')

    # case of no value
    if len(entry) == 1:
        res = "Currency not found for this date or not supported"
    else:
        res = entry[1].find_elements(By.TAG_NAME, 'td')[3].text
        if res == "":
            res = "Selling rate column empty"
except Exception as e:
    if e.__class__.__name__ == "NoSuchElementException":
        res = "Currency not found or not supported"
    else:
        
        res = "Unkown Error"

driver.quit()

file_path = 'result.txt'

with open(file_path, 'a') as file:
    file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, {date}, {args.currency}, {res}\n")
