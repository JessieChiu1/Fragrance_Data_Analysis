from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm

# ===========
# init driver
# ===========

url = "https://www.fragrantica.com/search/"
# url = "https://www.fragrantica.com/noses/"
# url = "https://www.fragrantica.com/perfume/By-Kilian/Angels-Share-62615.html"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--ignore-certificate-error")
chrome_options.add_argument("--ignore-ssl-errors")
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(options=chrome_options)
# driver.get(url)

# =================================
# Navigating Fragrantic's fragrance
# =================================
# init wait
wait = WebDriverWait(driver, timeout=30)
# wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
#
# # I usually don't like to use XPATH but there is no good way to access this element
# total_frag = driver.find_element(By.XPATH, '//*[@id="offCanvasRight"]/div[3]/b[1]')
# print(f"Total Frag is {total_frag.text}")

# Getting a list of perfumers
# ===========================

# # this is the container with all the perfumers
# container = driver.find_element(By.XPATH, '//*[@id="main-content"]/div[1]/div[1]/div')
#
# all_perfumers = driver.find_elements(By.CSS_SELECTOR, '.cell.small-12.medium-4')
#
# # for some reason, selenium is picking up the login link, so I removed it
# all_perfumers = all_perfumers[:-1]
#
# # find all perfumer's link
# print(f"Let's find all {len(all_perfumers)} perfumers")
#
# all_perfumers = [perfumer.find_element(By.TAG_NAME, "a").text for perfumer in tqdm(all_perfumers)]
#
# print(all_perfumers[0])
#
# print(f"Done, we have {len(all_perfumers)} perfumers to go through now")

# Getting a list of fragrances
# ============================
# it will just be easier to reconstruct the url

# all_perfumers = [f"?nosevi={name.replace(' ', '%20')}" for name in all_perfumers]
# print(all_perfumers[0])

# driver.quit()
# driver = webdriver.Chrome(options=chrome_options)
print("Opening search page...")

# driver.get(url=f"https://www.fragrantica.com/search/{all_perfumers[0]}")
driver.get(url="https://www.fragrantica.com/search/?nosevi=Alberto%20Morillas")
print("search page loaded....")

show_more_results_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".ais-InfiniteHits button")))
print(show_more_results_button.text)

while show_more_results_button.get_attribute("disabled") != "true":
    try:
        # Find the button and scroll it into view then click it
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".ais-InfiniteHits button")))
        show_more_results_button = driver.find_element(By.CSS_SELECTOR, ".ais-InfiniteHits button")
        # Use WebDriverWait to wait for the button to be clickable
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", show_more_results_button)
        show_more_results_button.click()
    except ElementClickInterceptedException as e:
        print("google ad iframe blocking the button, scrolling to button....")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", show_more_results_button)

print("getting fragrances' link")
all_fragrance = driver.find_elements(By.CSS_SELECTOR, ".cell.card.fr-news-box")

all_fragrance = [fragrance.find_element(By.CSS_SELECTOR, ".card-section a").get_attribute("href") for fragrance in
                 all_fragrance]

print(all_fragrance)

# driver.quit()
