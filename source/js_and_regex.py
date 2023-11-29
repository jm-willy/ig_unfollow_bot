import re
from random import randint

from selenium.common.exceptions import JavascriptException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from time_utils import nap
from xpaths import window_class_name

dict_js = {
    'users window innerHTML': 'return document.getElementsByClassName("{}")[0].innerHTML;'.format(window_class_name),
    'scroll users': 'document.getElementsByClassName("{}")[0].scrollBy(0, {})',
    'reload': 'location.reload()',
    'click': 'arguments[0].click();',
    'scroll view by xpath': 'document.evaluate("{}", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).'
                            'singleNodeValue.scrollIntoView({behavior: "smooth", block: "center", inline: "center"})',
}

dict_regex = {
    'users': 'notranslate _a6hd" href="/(.*?)/" role="link',
}


def get_users_from_page_source(browser):
    wait = WebDriverWait(browser, randint(7, 16))
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, window_class_name)))
    try:
        source = browser.execute_script(dict_js['users window innerHTML'])
    except (JavascriptException, TypeError):
        nap(0.66)
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, window_class_name)))
        source = browser.execute_script(dict_js['users window innerHTML'])

    matches = re.findall(dict_regex['users'], source)
    output_ = []
    for i in matches:
        if i not in output_:
            output_.append(i)
    return output_


def js_reload(browser):
    nap(4.6)
    browser.execute_script(dict_js['reload'])
    nap(6.4)
    return


def js_scroll_into_view_by_xpath(browser, xpath):
    browser.execute_script(dict_js['scroll view by xpath'].format(xpath))
    nap(0.13)
    return


def js_click_by_xpath(browser, xpath):
    element = browser.find_element('xpath', xpath)
    browser.execute_script("arguments[0].click();", element)
    nap(0.23)
    return
