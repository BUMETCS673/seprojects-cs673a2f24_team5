from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import time

FRONTEND_URL = "http://localhost:3001"
API_URL = "http://127.0.0.1:5001"

options = Options()
# options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
driver.get(FRONTEND_URL)
wait = WebDriverWait(driver, 10)

try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[aria-labelledby="button-label"]'))
    )

    # Google login
    google_login_button = driver.find_element(By.CSS_SELECTOR, '[aria-labelledby="button-label"]')
    # google_login_button.click()

    # Upload Resume
    upload_div = driver.find_element(By.CSS_SELECTOR, "div[style*='cursor: pointer'][style*='display: flex']")
    # upload_div.click()

    wait = WebDriverWait(driver, 10)
    file_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']")))

    file_path = "/Users/caozhen/PycharmProjects/seprojects-cs673a2f24_team5/be_repo/tests/test_resume.pdf"
    file_input.send_keys(file_path)

    alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
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
    textarea = WebDriverWait(driver, 10).until(
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
