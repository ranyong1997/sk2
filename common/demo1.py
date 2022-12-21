from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

d = DesiredCapabilities.CHROME
d['goog:loggingPrefs'] = {'browser': 'ALL'}

driver = webdriver.Chrome(desired_capabilities=d)
driver.maximize_window()
driver.get(url='https://course.icve.com.cn/learnspace/learn/learn/templateeight/index.action?params.courseId=1754b2c1a83f4268a668e959b9d3941a___&params.templateType=8&params.templateStyleType=0&params.template=templateeight&params.classId=&params.tplRoot=learn')

print(driver.get_log("browser"))
# driver.get_cookies()
print(driver.get_cookies())