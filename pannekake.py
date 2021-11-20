from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.common.exceptions import WebDriverException,NoSuchElementException
from time import sleep
from datetime import datetime
date_prefix = datetime.today().strftime('%Y-%m-%d')

#Pannekaketesten!
try:
    with webdriver.Firefox() as driver:
        driver.get("https://www.tine.no/oppskrifter")
        searchbar = driver.find_element_by_xpath("//form[1]/input[1]")
        searchbar.send_keys("Pannekaker")
        searchbar.send_keys(Keys.RETURN)
        sleep(5) #Waiting for search results
        driver.find_element_by_partial_link_text("grunnoppskrift").click()
        sleep(5)
        src = driver.page_source
        driver.save_screenshot(date_prefix+'-pannekake-screenshot.png')
        assert("For laktosefri oppskrift") in src
        assert("en god oppskrift på pannekaker") in src
        assert("Det går fint an å lage en grovere variant") in src
        assert("Smelt litt smør i en varm stekepanne") in src
        assert("Lag gjerne stor porsjon") in src
        pass
    pass
except WebDriverException:
    print("Woops")
