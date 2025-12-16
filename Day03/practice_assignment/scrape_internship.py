from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ----------------------------
# Browser setup
# ----------------------------
chrome_options = Options()
#chrome_options.add_argument("--headless")  # remove for visible browser

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 15)

# ----------------------------
# Step 1: Open Sunbeam website
# ----------------------------
driver.get("https://sunbeaminfo.in")
print("Home Page:", driver.title)

# ----------------------------
# Step 2: Open Internship page
# ----------------------------
driver.get("https://sunbeaminfo.in/internship")
print("Internship Page:", driver.title)

# =====================================================
# PART 1: Fetch INTERNSHIP BATCHES table
# =====================================================
print("\n--- Internship Batches ---")

wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "tbody tr")))
batch_rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")

for row in batch_rows:
    cols = row.find_elements(By.TAG_NAME, "td")

    if len(cols) < 8:
        continue

    batch_info = {
        "Sr No": cols[0].text,
        "Batch": cols[1].text,
        "Batch Duration": cols[2].text,
        "Start Date": cols[3].text,
        "End Date": cols[4].text,
        "Time": cols[5].text,
        "Fees": cols[6].text,
        "Brochure": cols[7].text
    }

    print(batch_info)

# =====================================================
# PART 2: Fetch AVAILABLE INTERNSHIP PROGRAMS table
# =====================================================
print("\n--- Available Internship Programs ---")

# Scroll to programs section
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

program_table = wait.until(
    EC.presence_of_element_located((By.XPATH, "//table[contains(@class,'table')]"))
)

program_rows = program_table.find_elements(By.TAG_NAME, "tr")

for row in program_rows:
    cols = row.find_elements(By.TAG_NAME, "td")

    if len(cols) < 3:
        continue

    program_info = {
        
        "Technology": cols[0].text,
        "Aim": cols[1].text,
        "Prerequisite": cols[2].text,
        "Learning": cols[3].text,
        "Location": cols[4].text
    }

    print(program_info)

driver.quit()
