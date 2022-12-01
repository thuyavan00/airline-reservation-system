from selenium import webdriver
from selenium.webdriver.common.by import By
import pytest

@pytest.fixture()
def env_setup():
    global driver
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options, executable_path="path/to/executable")
    driver.get("http://127.0.0.1:5000/login")
    driver.maximize_window()
    yield
    driver.close()
#TC_ARS_register_001
def test_verify_register_001(env_setup):
    driver.find_element(By.NAME, "username").send_keys("tk")
    driver.find_element(By.NAME, "password").send_keys("qwerty")
    driver.find_element(By.ID, "regbit").click()
    alert = driver.switch_to.alert
    text = alert.text
    alert.accept()
    print(text)
    driver.back()
#TC_ARS_register_002
def test_verify_register_002(env_setup):
    driver.find_element(By.NAME, "username").send_keys("tk")
    driver.find_element(By.NAME, "password").send_keys("qwerty")
    driver.find_element(By.ID, "regbit").click()
    alert = driver.switch_to.alert
    text = alert.text
    alert.accept()
    print(text)
    driver.back()
#TC_ARS_register_003
def test_verify_register_003(env_setup):
    driver.find_element(By.NAME, "username").send_keys("")
    driver.find_element(By.NAME, "password").send_keys("")
    driver.find_element(By.ID, "regbit").click()
    alert = driver.switch_to.alert
    text = alert.text
    alert.accept()
    print(text)
    driver.back()
#TC_ARS_register_004
def test_verify_register_004(env_setup):
    driver.find_element(By.NAME, "username").send_keys("test@211")
    driver.find_element(By.NAME, "password").send_keys("qwerty12")
    driver.find_element(By.ID, "regbit").click()
    alert = driver.switch_to.alert
    text = alert.text
    alert.accept()
    print(text)
    driver.back()
#check the url
    assert driver.current_url == "http://127.0.0.1:5000/login"
