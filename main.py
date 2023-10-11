from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm


# ===========
# init driver
# ===========

url = "https://www.fragrantica.com/noses/"
# url = "https://www.fragrantica.com/perfume/By-Kilian/Angels-Share-62615.html"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--ignore-certificate-error")
chrome_options.add_argument("--ignore-ssl-errors")
driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

# =================================
# Navigating Fragrantic's fragrance
# =================================
# init wait
wait = WebDriverWait(driver, timeout=30)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))

# I usually don't like to use XPATH but there is no good way to access this element
total_frag = driver.find_element(By.XPATH, '//*[@id="offCanvasRight"]/div[3]/b[1]')
print(f"Total Frag is {total_frag.text}")


# Getting a list of perfumers
# ===========================

perfumer_list = []

# this is the container with all the perfumers
container = driver.find_element(By.XPATH, '//*[@id="main-content"]/div[1]/div[1]/div')

all_perfumers = driver.find_elements(By.CSS_SELECTOR, '.cell.small-12.medium-4')

# for some reason, selenium is picking up the login link, so I removed it
all_perfumers = all_perfumers[:-1]

# find all perfumer's link
print(f"Let's find all {len(all_perfumers)} perfumers")
for perfumer in tqdm(all_perfumers):
    a_tag = perfumer.find_element(By.TAG_NAME, "a")
    perfumer_list.append(a_tag.text)
    print(f"Type of 'a_tag.text': {type(a_tag.text)}")
    print(f"Type of 'perfumer_list[-1]': {type(perfumer_list[-1])}")

print(f"Done, we have {len(perfumer_list)} perfumers to go through now")

# Getting a list of fragrances
# ============================

# okay for some reason, I keep running into error trying to find the perfumer search input element
# so after some googling to no avail, I decided to just reconstruct the url....

for perfumer in all_perfumers:
    print(f"{perfumer}: type({perfumer}) return {type(perfumer)}")


# I tried using driver.close() then going to the new url, but it is running into errors, so I decide to quit the
# webdriver and go to the link from a new driver session again, and it resolves the issue

# driver.quit()
# print("Opening search page....")
# driver = webdriver.Chrome(options=chrome_options)
# driver.get(url=f"https://www.fragrantica.com/search/{all_perfumers[0]}")
# wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))
#
# print("locating search by perfumer input box...")
