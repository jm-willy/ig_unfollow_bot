# -*- coding: UTF-8 -*-
import os
import sys
from random import randint
from time import sleep

import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options

from browsing_util import go_to_profile
from browsing_util import stop_until_user_input
from relations import UnFollow
from time_utils import date_time_print
from users_to_not_unfollow import not_unfollow_list

user_data_path = 'C:/Users/MyUser/AppData/Local/Google/Chrome/User Data/Default'
driver_path = os.getcwd() + 'chromedriver.exe'
chrome_options = Options()
chrome_options.add_argument("--user-data-dir={}".format(user_data_path))
browser = uc.Chrome(version_main=109, executable_path=driver_path, options=chrome_options)
browser.maximize_window()
browser.implicitly_wait(randint(7, 15))
sleep(0.33)

###########################

go_to_profile(browser)
stop_until_user_input()
uf = UnFollow(exceptions_list=not_unfollow_list)
uf.load_relations(skip_followers=True)
uf.get_them(browser)
uf.get_them(browser, unfollow=True)
uf.get_them_loop(browser, unfollow=True)
date_time_print('Finished')
stop_until_user_input()
sys.exit()
