from random import randint
from random import uniform
from time import sleep

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from js_and_regex import dict_js
from time_utils import date_time_print
from time_utils import nap
from xpaths import dict_xpaths
from xpaths import my_username
from xpaths import window_class_name


def go_to_profile(browser):
    increment = 6
    target_url = 'https://www.instagram.com/{}/'.format(my_username)
    while browser.current_url != target_url:
        browser.get(target_url)
        sleep(increment)
        increment += increment
    date_time_print('Now in profile page')
    while not browser.find_element('xpath', dict_xpaths['profile icon']).is_displayed:
        date_time_print('Not logged, log in manually, go to profile and resume')
        stop_until_user_input()
    date_time_print('Logged in')
    nap(2.3)
    return


def scroll_users(browser, slow=False):
    # viewport_height = int(browser.execute_script('return window.innerHeight;'))
    wait = WebDriverWait(browser, randint(11, 53))
    try:
        wait.until(EC.visibility_of_element_located((By.XPATH, dict_xpaths['users relation window'])))
        win_height = int(browser.find_element('xpath', dict_xpaths['users relation window']).size['width'])
    except NoSuchElementException:
        wait.until(EC.visibility_of_element_located((By.XPATH, dict_xpaths['users relation window'])))
        win_height = int(browser.find_element('xpath', dict_xpaths['users relation window']).size['width'])

    if slow:
        browser.execute_script(
            dict_js['scroll users'].format(window_class_name, (win_height * uniform(0.55, 1)))
        )
    else:
        browser.execute_script(
            dict_js['scroll users'].format(window_class_name, (win_height * uniform(1.2, 3.4)))
        )
        nap(0.07)
    nap(0.04)
    return


def stop_until_user_input(secs=40):
    while True:
        x = input('Paused, should the bot continue? Y/N :')
        if x == 'y' or x == 'Y':
            break
        else:
            date_time_print('sleeping for {} secs, then asking again'.format(secs))
            sleep(secs)
    return


def format_thousands_str(string):
    result = []
    for i in string:
        if i != ',':
            result.append(i)
    result = ''.join(result)
    return int(result)


def wait_clickable_click(browser, xpath):
    wait = WebDriverWait(browser, randint(8, 17))
    wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
    wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    browser.find_element('xpath', xpath).click()
    nap(0.14)
    return
