from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

#import general functions for tests
from commonFunctions import setCurrentTestDriver
from commonFunctions import assertTryExcept

#import setup and current Test Run Default Parameters - see setup.yaml
import yaml
with open("Setup.yaml", "r") as yaml_file:
    setup = yaml.safe_load(yaml_file)
currentTestDriver = setup["testDriver"]
currentTestSiteUrl = setup["testSiteURL"]
currentTestUser = setup["testUser"]
currentReportsDirectory = setup["testReportsDirectory"]

#set baseURLs
baseURL = setup[currentTestSiteUrl]

#import selectors
from pagesSelectors.accountPages import *
from pagesSelectors.mainPage import *

def test_SmokeRegisteredUserCanLogin():
    #ID: 11
    #URL: https://app.qase.io/case/wdt-11

    driver = setCurrentTestDriver(currentTestDriver)
    
    #1.Open the Main Page
    driver.get(baseURL)
    driver.maximize_window()
    assertTryExcept(driver, driver.title, pageTitle_MainPage_Desktop)

    #2. Click Accept cookies
    driver.find_element(By.XPATH, AcceptCookie_button_byXPATH_MainPage_Desktop).click()

    #3. Click on "Sign In" in the header
    driver.find_element(By.XPATH, Account_link_byXPATH_MainPage_Desktop).click()
    time.sleep(10)

    #expected: account/login page is opened
    assertTryExcept(driver, driver.title, LoginPageTitle_Text_Account_Desktop)

    #4. Enter the user email
    driver.find_element(By.NAME, Email_Input_byNAME_Account_Desktop).send_keys(setup["Users"][currentTestUser]["email"])

    #5. Check "Enter your password" option
    driver.find_element(By.NAME, Password_Input_byNAME_Account_Desktop).send_keys(setup["Users"][currentTestUser]["password"])

    #6. Click "LogIn" button
    driver.find_element(By.XPATH, LogIn_Button_byXPATH_Account_Desktop).click()
    time.sleep(10)

    #expected: Main page is opened
    assertTryExcept(driver, driver.title, pageTitle_MainPage_Desktop)

    #7. Check the header
    #expected: User name is shown in the Header

    assertTryExcept(driver, driver.find_element(By.XPATH, UserName_text_byXPATH_MainPage_Desktop).text, setup["Users"][currentTestUser]["shortName"])

    #8. Hower over the user name
    ActionChains(driver).move_to_element(driver.find_element(By.XPATH, UserName_text_byXPATH_MainPage_Desktop)).perform()

    #9. Click on setting link in the popup
    driver.find_element(By.XPATH, "//p[contains(text(),'Podešavanje naloga')]").click()
    time.sleep(10)
    
    #10. Check User Full Name

    #expected: User fullname is shown
    assertTryExcept(driver, driver.find_element(By.XPATH, Imeiprezime_Text_byXPATH_Account_Desktop).text, setup["Users"][currentTestUser]["fullName"])
    
    driver.close()