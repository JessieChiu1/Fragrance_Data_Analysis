from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm
import json
import html


# ===========
# init driver
# ===========

url = "https://www.fragrantica.com/noses/"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--ignore-certificate-error")
chrome_options.add_argument("--ignore-ssl-errors")
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

# =================================
# Navigating Fragrantic's fragrance
# =================================
# init wait
wait = WebDriverWait(driver, timeout=30)
wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

# I usually don't like to use XPATH but there is no good way to access this element
total_frag = driver.find_element(By.XPATH, '//*[@id="offCanvasRight"]/div[3]/b[1]')
print(f"Total Frag is {total_frag.text}")

# Getting a list of perfumers
# ===========================

# this is the container with all the perfumers
container = driver.find_element(By.XPATH, '//*[@id="main-content"]/div[1]/div[1]/div')

all_perfumers = driver.find_elements(By.CSS_SELECTOR, '.cell.small-12.medium-4')

# for some reason, selenium is picking up the login link, so I removed it
all_perfumers = all_perfumers[:-1]

# find all perfumer's link
print(f"Let's find all {len(all_perfumers)} perfumers")

all_perfumers = [perfumer.find_element(By.TAG_NAME, "a").text for perfumer in tqdm(all_perfumers)]
decoded_names = [html.unescape(name) for name in all_perfumers]

with open("perfumers_name.json", mode="w") as file:
    data = {
        "perfumers": decoded_names
    }
    json.dump(data, file, indent=4)

print(f"Done, we have {len(all_perfumers)} perfumers to go through now")

driver.quit()

