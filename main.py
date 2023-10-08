from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm


# ===========
# init driver
# ===========

url = "https://www.fragrantica.com/noses/"
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

# I wish the site has better className/ID But this is what we have to work with
perfumer_list = []

# this is the container with all the perfumers
container = driver.find_elements(By.XPATH, '//*[@id="main-content"]/div[1]/div[1]')

# this finds all the perfumers
all_perfumers = driver.find_elements(By.CSS_SELECTOR, '.cell.small-12.medium-4')


print(f"Let's find all {len(all_perfumers)} perfumers")
for perfumer in tqdm(all_perfumers):
    a_tag = perfumer.find_element(By.TAG_NAME, "a")
    perfumer_list.append(a_tag.get_attribute("href"))

print(f"Done, we have {len(perfumer_list)} perfumers to go through now")
