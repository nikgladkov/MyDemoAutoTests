#import modules
import os
from selenium import webdriver
import time
from datetime import datetime
from datetime import date
import sys
import csv

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

#functions
def setCurrentTestDriver(currentTestDriver):
    match currentTestDriver:
        case "Chrome":
            driver = webdriver.Chrome()
        # case: "Firefox":
        # case: "Edge":
        # case: ""
    return driver

def makeScreenshot(driver, directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    time.sleep(1)
    driver.save_screenshot(f"{directory}\screenshot_{datetime.now().strftime("%d%m%Y_%H%M%S")}.png")

def scrollThePage(driver, direction):
    
    current_height = driver.execute_script("return window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight;")
    
    match direction:
        case "down":
            driver.execute_script(f"window.scrollTo(0, {current_height});")
        case "up":
            driver.execute_script(f"window.scrollTo(0, -{current_height});")
        case "bottom":
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        case "top":
            driver.execute_script("window.scrollTo(0, 0);")
        case _:
            driver.execute_script(f"window.scrollTo(0, {current_height});")

def assertTryExcept(driver, current, expected):
    try:
        assert current == expected
    except AssertionError as e:
        makeScreenshot(driver, currentReportsDirectory)
        sys.exit(1)

def saveURLScreenshotInfoToTestReport(driver,testName,testRunid,StepInfo="-",testResult="-"):
    curTime = datetime.now().strftime("%H%M")
    curTestRunName = testName + str(date.today()) + "_" + testRunid
    curStepInfo = StepInfo
    curTestResult = testResult
    curUrl = driver.current_url
    curFilePath = makeScreenshot(driver, currentReportsDirectory)

    data = [
        [curTime,curTestRunName,curStepInfo,curTestResult,curUrl,curFilePath]
    ]

    file_path = f"{currentReportsDirectory}/testReport.csv"

    with open(file_path, mode='a+', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)
        file.close