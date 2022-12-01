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
#TC_ARS_Login_001
def test_verify_login_001(env_setup):
    driver.find_element(By.NAME, "username").send_keys("tk")
    driver.find_element(By.NAME, "password").send_keys("qwerty")
    driver.find_element(By.ID, "logbut").click()
    driver.back()
#TC_ARS_Login_002
def test_verify_login_002(env_setup):
    driver.find_element(By.NAME, "username").send_keys("tk")
    driver.find_element(By.NAME, "password").send_keys("qwe55")
    driver.find_element(By.ID, "logbut").click()
    driver.back()
#TC_ARS_Login_003
def test_verify_login_003(env_setup):
    driver.find_element(By.NAME, "username").send_keys("tk12345")
    driver.find_element(By.NAME, "password").send_keys("qwerty")
    driver.find_element(By.ID, "logbut").click()
    driver.back()
#TC_ARS_Login_004
def test_verify_login_004(env_setup):
    driver.find_element(By.NAME, "username").send_keys("test@12")
    driver.find_element(By.NAME, "password").send_keys("qwerty12")
    driver.find_element(By.ID, "logbut").click()
    driver.back()
#check the url
    assert driver.current_url == "http://127.0.0.1:5000/login"
