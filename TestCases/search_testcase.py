from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.common.by import By
import pytest

@pytest.fixture()
def env_setup():
    global driver
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    driver.get("http://127.0.0.1:5000/land")
    driver.maximize_window()
    yield
    driver.close()
    
#TC_ARS_Search_001
def test_verify_search_001(env_setup):
    driver.find_element(By.NAME, "ori").send_keys("Vancouver")
    driver.find_element(By.NAME, "dest").send_keys("London")
    driver.find_element(By.NAME, "date").send_keys("12-12-2022")
    driver.find_element(By.ID, "sbut").click()
    driver.back()

#TC_ARS_Search_002
def test_verify_search_002(env_setup):
    driver.find_element(By.NAME, "ori").send_keys("Hello")
    driver.find_element(By.NAME, "dest").send_keys("London")
    driver.find_element(By.NAME, "date").send_keys("12-12-2022")
    driver.find_element(By.ID, "sbut").click()
    driver.back()

#TC_ARS_Search_003
def test_verify_search_003(env_setup):
    driver.find_element(By.NAME, "ori").send_keys("Vancouver")
    driver.find_element(By.NAME, "dest").send_keys("Hello")
    driver.find_element(By.NAME, "date").send_keys("12-12-2022")
    driver.find_element(By.ID, "sbut").click()
    driver.back()

#TC_ARS_Search_004
def test_verify_search_004(env_setup):
    driver.find_element(By.NAME, "ori").send_keys("Vancouver")
    driver.find_element(By.NAME, "dest").send_keys("London")
    driver.find_element(By.NAME, "date").send_keys("11010-2022")
    driver.find_element(By.ID, "sbut").click()
    driver.back()

#TC_ARS_Search_005
def test_verify_search_005(env_setup):
    driver.find_element(By.NAME, "ori").send_keys("Hello")
    driver.find_element(By.NAME, "dest").send_keys("bye")
    driver.find_element(By.NAME, "date").send_keys("12-12-2022")
    driver.find_element(By.ID, "sbut").click()
    driver.back()

#TC_ARS_Search_006
def test_verify_search_006(env_setup):
    driver.find_element(By.NAME, "ori").send_keys("Hello")
    driver.find_element(By.NAME, "dest").send_keys("bye")
    driver.find_element(By.NAME, "date").send_keys("10-102022")
    driver.find_element(By.ID, "sbut").click()
    driver.back()


