import time
from selenium import webdriver

#ADDING WEB DRIVER
str1 = "hi"
web_driver = webdriver.Chrome(executable_path = 'D:\Downloads\chromedriver_win32\chromedriver.exe')
web_driver.get("https://web.whatsapp.com")

time.sleep(10)

#Find Group Name

user_name = 'Zenon'
user = web_driver.find_element_by_xpath('//span[@title="{}"]'.format(user_name))
user.click()

message = web_driver.find_element_by_xpath('//div[@class="_2A8P4"]')
message.send_keys(str1)


message_submit = web_driver.find_element_by_xpath('//button[@class="_1E0Oz"]')
message_submit.click()
