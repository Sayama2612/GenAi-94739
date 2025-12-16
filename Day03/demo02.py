from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()

driver.get("https://www.flipkart.com/")
print("Initial page title :", driver.title)

driver.implicitly_wait(5)

search_box = driver.find_element(By.NAME, "q")

for ch in "Sneakers":
    search_box.send_keys(ch)
    time.sleep(0.2)
#search_box.send_keys("Sneakers")
search_box.send_keys(Keys.RETURN)    

print("Later page title :", driver.title)

time.sleep(8)
driver.quit()