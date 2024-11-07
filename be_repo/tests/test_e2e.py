from selenium import webdriver
import chromedriver_autoinstaller
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from pyvirtualdisplay import Display

FRONTEND_URL = "http://localhost:3001"

display = Display(visible=0, size=(800, 800))
display.start()

chromedriver_autoinstaller.install()

chrome_options = webdriver.ChromeOptions()
options = [
    "--window-size=1200,1200",
    "--ignore-certificate-errors"
    "--headless",
]

for option in options:
    chrome_options.add_argument(option)

driver = webdriver.Chrome(options=chrome_options)

driver.get(FRONTEND_URL)
wait = WebDriverWait(driver, 20)

try:
    wait.until(
        lambda driver: driver.execute_script("return document.readyState") == "complete"
    )

    # Google login
    # google_login_button = driver.find_element(By.CSS_SELECTOR, '[aria-labelledby="button-label"]')
    # google_login_button.click()

    # Upload Resume
    upload_div = driver.find_element(By.CSS_SELECTOR, "div[style*='cursor: pointer'][style*='display: flex']")
    # upload_div.click()

    file_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']")))

    file_path = os.path.join(os.path.dirname(__file__), 'test_resume.pdf')
    file_input.send_keys(file_path)

    alert = wait.until(EC.alert_is_present())
    alert_text = alert.text
    assert "Resume uploaded successfully" in alert_text
    alert.accept()

    # Analyze resume
    analyze_button = driver.find_element(By.CLASS_NAME, "cursor-pointer")
    analyze_button.click()

    submit_button = driver.find_element(By.CLASS_NAME, "mt-6")
    submit_button.click()

    time.sleep(20)

    keywords = [
        "Analysis Result",
        "Consistency and Chronology",
        "Education",
        "Project and Work Experience",
        "Resume Structure and Presentation",
        "Skills and Certifications",
        "Soft Skills"
    ]

    elements = driver.find_elements(By.CLASS_NAME, "font-bold")
    content_text = " ".join([element.text for element in elements])
    for keyword in keywords:
        count = content_text.count(keyword)
        assert count == 1, f"'{keyword}' does not appear exactly twice in the content (found {count} times)"

    # Analyze resume with JD
    analyze_button.click()
    textarea = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "textarea.w-full.h-40.p-4.border-2"))
    )
    textarea.send_keys("Sample job description text")
    submit_button = driver.find_element(By.CLASS_NAME, "mt-6")
    submit_button.click()

    time.sleep(20)

    elements = driver.find_elements(By.CLASS_NAME, "font-bold")
    content_text = " ".join([element.text for element in elements])
    for keyword in keywords:
        count = content_text.count(keyword)
        assert count == 2, f"'{keyword}' does not appear exactly twice in the content (found {count} times)"

finally:
    driver.quit()
