import pytest
import os
import time
from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyvirtualdisplay import Display

FRONTEND_URL = "http://localhost:3001"
keywords = [
    "Analysis Result",
    "Consistency and Chronology",
    "Education",
    "Project and Work Experience",
    "Resume Structure and Presentation",
    "Skills and Certifications",
    "Soft Skills"
]


@pytest.fixture(scope="module")
def driver():
    # Start display
    display = Display(visible=0, size=(800, 800))
    display.start()

    # Install and set up Chrome driver
    chromedriver_autoinstaller.install()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--window-size=1200,1200")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()
    display.stop()


@pytest.fixture
def wait(driver):
    return WebDriverWait(driver, 20)


def test_resume_upload(driver, wait):
    driver.get(FRONTEND_URL)
    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

    # Upload resume
    upload_div = driver.find_element(By.CSS_SELECTOR, "div[style*='cursor: pointer'][style*='display: flex']")
    file_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']")))

    file_path = os.path.join(os.path.dirname(__file__), 'test_resume.pdf')
    file_input.send_keys(file_path)

    # Check for alert after upload
    alert = wait.until(EC.alert_is_present())
    alert_text = alert.text
    assert "Resume uploaded successfully" in alert_text
    alert.accept()


def test_analyze_resume(driver, wait):
    # Analyze resume
    analyze_button = driver.find_element(By.CLASS_NAME, "cursor-pointer")
    analyze_button.click()

    submit_button = driver.find_element(By.CLASS_NAME, "mt-6")
    submit_button.click()

    time.sleep(20)  # Ensure analysis completes

    elements = driver.find_elements(By.CLASS_NAME, "font-bold")
    content_text = " ".join([element.text for element in elements])
    for keyword in keywords:
        count = content_text.count(keyword)
        assert count == 1, f"'{keyword}' does not appear exactly once in the content (found {count} times)"


def test_analyze_resume_with_jd(driver, wait):
    # Analyze resume with JD
    analyze_button = driver.find_element(By.CLASS_NAME, "cursor-pointer")
    analyze_button.click()
    textarea = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "textarea.w-full.h-40.p-4.border-2")))
    textarea.send_keys("Sample job description text")

    submit_button = driver.find_element(By.CLASS_NAME, "mt-6")
    submit_button.click()

    time.sleep(20)  # Ensure analysis completes

    elements = driver.find_elements(By.CLASS_NAME, "font-bold")
    content_text = " ".join([element.text for element in elements])
    for keyword in keywords:
        count = content_text.count(keyword)
        assert count == 2, f"'{keyword}' does not appear exactly twice in the content (found {count} times)"
