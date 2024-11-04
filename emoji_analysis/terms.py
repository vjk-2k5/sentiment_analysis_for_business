from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import time

# Set up Selenium WebDriver (e.g., for Chrome)
driver = webdriver.Chrome()  # Ensure you have the correct ChromeDriver for your version of Chrome

# Open the Investopedia dictionary page
url = "https://www.investopedia.com/financial-term-dictionary-4769738"
driver.get(url)

# Give the page some time to load
time.sleep(5)

# Extract terms
terms = []
elements = driver.find_elements(By.CSS_SELECTOR, "a[data-testid='dictionary-term']")

# Loop through the elements and extract the text (terms)
for element in elements:
    terms.append(element.text)

# Close the driver
driver.quit()

# Write the terms to a CSV file
with open('financial_terms_selenium.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Term"])  # Header row
    
    # Write each term to the CSV
    for term in terms:
        writer.writerow([term])

print("CSV file with terms has been created.")
