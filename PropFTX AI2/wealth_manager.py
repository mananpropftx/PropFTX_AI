import csv
from fpdf import FPDF
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
url = "https://www.sebi.gov.in/sebiweb/other/OtherAction.do?doRecognisedFpi=yes&intmId=33"
driver.get(url)

wait = WebDriverWait(driver, 20)
all_data = []

def extract_current_page_data():
    wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "card-table-left")))
    entities = driver.find_elements(By.CLASS_NAME, "card-table-left")
    
    for entity in entities:
        card_views = entity.find_elements(By.CLASS_NAME, "card-view")
        entity_data = {}
        for card in card_views:
            try:
                title = card.find_element(By.XPATH, "title").text.strip()
                value = card.find_element(By.CLASS_NAME, "value").text.strip()
                entity_data[title] = value
            except Exception as e:
                print(f"Error extracting a field: {e}")
        if entity_data:
            all_data.append(entity_data)

# Extract page 1
extract_current_page_data()

# Pages 2 to 5
for page_num in range(2, 6):
    print(f"Navigating to page {page_num}...")
    driver.execute_script(f"searchFormFpi('n', '{page_num - 1}');")
    time.sleep(2)
    extract_current_page_data()

driver.quit()

# --- Save to CSV ---
csv_file = "fpi_data.csv"
fieldnames = set()
for item in all_data:
    fieldnames.update(item.keys())
fieldnames = list(fieldnames)

with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for entry in all_data:
        writer.writerow(entry)

print(f"Data saved to CSV: {csv_file}")

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=10)

for idx, entry in enumerate(all_data, start=1):
    pdf.set_font("Arial", size=10, style='B')
    pdf.cell(200, 10, txt=f"Entity {idx}", ln=True)
    pdf.set_font("Arial", size=10)
    for key, val in entry.items():
        pdf.multi_cell(0, 8, txt=f"{key}: {val}")
    pdf.ln(5)

pdf_file = "fpi_data.pdf"
pdf.output(pdf_file)

print(f"Data saved to PDF: {pdf_file}")
