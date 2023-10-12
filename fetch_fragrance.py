import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm
import json

# ===================
# fetch perfumer.json
# ===================
try:
    with open("perfumers_name.json", mode="r") as file:
        data = json.load(file)
        all_perfumers = data["perfumers"]
except FileNotFoundError:
    print("No perfumers.json found, please run fetch_perfumer.py first")
    raise

print(f"This is just testing if we are loading the names correctly, the last perfumer has a Chinese name: {all_perfumers[-1]}")

# ===========
# init driver
# ===========

url = "https://www.fragrantica.com/search/"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--ignore-certificate-error")
chrome_options.add_argument("--ignore-ssl-errors")
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

# Getting a list of fragrances
# ============================

wait = WebDriverWait(driver, timeout=30)

all_fragrance = []

for perfumer in tqdm(all_perfumers):
    try:
        # uncheck all filter
        filtered_container = driver.find_element(By.XPATH,
                                                 '//*[@id="offCanvasLeftOverlap1"]/div/div/div[8]/div[2]/div/p/div/ul')
        all_checkbox = filtered_container.find_elements(By.TAG_NAME, "input")
        for checkbox in all_checkbox:
            if checkbox.is_selected():
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox)
                checkbox.click()

        # Filtering by the perfumer
        wait.until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Search perfumer name"]')))
        search_by_perfumer_input = driver.find_element(By.XPATH, '//input[@placeholder="Search perfumer name"]')
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", search_by_perfumer_input)
        for char in perfumer:
            search_by_perfumer_input.send_keys(char)
            time.sleep(0.1)

        # Click the search button to filter
        time.sleep(1)
        filtered_container = driver.find_element(By.XPATH,
                                                 '//*[@id="offCanvasLeftOverlap1"]/div/div/div[8]/div[2]/div/p/div/ul')
        perfumer_checkbox = filtered_container.find_element(By.TAG_NAME, "input")
        perfumer_checkbox.click()

        # Click on the show more result button until all results are displayed
        show_more_results_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".ais-InfiniteHits button")))

        while show_more_results_button.get_attribute("disabled") != "true":
            try:
                # Find the button and scroll it into view then click it
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".ais-InfiniteHits button")))
                show_more_results_button = driver.find_element(By.CSS_SELECTOR, ".ais-InfiniteHits button")
                # Use WebDriverWait to wait for the button to be clickable
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", show_more_results_button)
                show_more_results_button.click()
            except ElementClickInterceptedException as e:
                print("Google ad iframe blocking the button, scrolling to button....")
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", show_more_results_button)

        # Adding all fragrances link to the list
        perfumer_frag = driver.find_elements(By.CSS_SELECTOR, ".cell.card.fr-news-box")
        perfumer_frag = [fragrance.find_element(By.CSS_SELECTOR, ".card-section a").get_attribute("href") for fragrance in perfumer_frag]
        all_fragrance.extend(perfumer_frag)
    except StaleElementReferenceException:
        perfumer_frag = driver.find_elements(By.CSS_SELECTOR, ".cell.card.fr-news-box")

# Save it to another JSON
with open("fragrances_link.json", mode="w") as file:
    data = {
        "fragrances": all_fragrance
    }
    json.dump(data, file, indent=4)
