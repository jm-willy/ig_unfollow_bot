from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import NoSuchElementException

from browsing_util import format_thousands_str
from browsing_util import scroll_users
from browsing_util import wait_clickable_click
from js_and_regex import get_users_from_page_source
from js_and_regex import js_click_by_xpath
from js_and_regex import js_reload
from js_and_regex import js_scroll_into_view_by_xpath
from save_relations import SaveRelations
from time_utils import date_time_print
from time_utils import nap
from xpaths import dict_xpaths


class UnFollow(SaveRelations):
    def __init__(self, exceptions_list):
        super().__init__()
        self.exceptions_list = exceptions_list
        self.followers_list = []
        self.following_list = []
        self.unfollowing_list = []
        self.already_unfollowed_list = []
        self.previous_len = -1
        self.current_len = 0
        self.displayed_followers_count = 0
        self.displayed_following_count = 0
        self.skip_followers = False
        self.displayed_rel_count = 0
        return

    def load_relations(self, skip_followers=False):
        self.skip_followers = skip_followers
        self.load_data()
        self.followers_list = self.data['followers']
        self.following_list = self.data['following']
        self.unfollowing_list = self.data['unfollow']
        return

    def f_append_users(self, browser, elements, unfollow):
        if not unfollow:
            for i in elements:
                i = i.get_attribute('href')[1:-1]
                if i not in self.followers_list:
                    self.followers_list.append(i)
            for i in get_users_from_page_source(browser):
                if i not in self.followers_list:
                    self.followers_list.append(i)

        elif unfollow:
            for i in elements:
                i = i.get_attribute('href')[1:-1]
                if i not in self.following_list:
                    self.following_list.append(i)
            for i in get_users_from_page_source(browser):
                if i not in self.following_list:
                    self.following_list.append(i)
                    if i not in self.unfollowing_list:
                        if i not in self.followers_list:
                            if i not in self.exceptions_list:
                                self.unfollowing_list.append(i)
        return

    def unfollow(self, browser):
        for i in self.unfollowing_list:
            if i not in self.already_unfollowed_list:
                xpath = dict_xpaths['user following unfollow button'].format(i)
                try:
                    wait_clickable_click(browser, xpath)
                except (ElementNotVisibleException, NoSuchElementException, ElementClickInterceptedException):
                    nap(2.6)
                    try:
                        js_scroll_into_view_by_xpath(browser, xpath)
                        wait_clickable_click(browser, xpath)
                    except (ElementNotVisibleException, ElementClickInterceptedException):
                        js_click_by_xpath(browser, xpath)
                finally:
                    self.data['unfollow'] = self.unfollowing_list
                nap(0.6)
                xpath = dict_xpaths['user following confirm unfollow button']
                wait_clickable_click(browser, xpath)
                nap(0.8)
                self.already_unfollowed_list.append(i)
                date_time_print('unfollowed: ', i)

        for i in self.already_unfollowed_list:
            if i in self.unfollowing_list:
                self.unfollowing_list.remove(i)
        return

    def loop_actions(self, browser, unfollow, append=True):
        if append:
            elements = browser.find_elements('xpath', dict_xpaths['usernames'])
            self.f_append_users(browser, elements, unfollow)
        if unfollow:
            self.unfollow(browser)
        scroll_users(browser, slow=unfollow)

        self.previous_len = self.current_len
        if not unfollow:
            self.current_len = len(self.followers_list)
        elif unfollow:
            self.current_len = len(self.following_list)
        return

    def get_relation_count(self, browser, unfollow):
        if not unfollow:
            self.displayed_followers_count = format_thousands_str(
                browser.find_element('xpath', dict_xpaths['followers count']).text
            )
            return self.displayed_followers_count
        elif unfollow:
            self.displayed_following_count = format_thousands_str(
                browser.find_element('xpath', dict_xpaths['following count']).text
            )
            return self.displayed_following_count

    def open_users(self, browser, unfollow):
        if not unfollow:
            if self.skip_followers:
                date_time_print('followers_list = ', len(self.followers_list))
                return

        self.displayed_rel_count = self.get_relation_count(browser, unfollow)
        if not unfollow:
            if not self.skip_followers:
                if self.displayed_rel_count > len(self.followers_list):
                    self.empty_data()
                    self.followers_list.clear()
                date_time_print('getting followers')
            date_time_print('{} followers count displayed'.format(self.displayed_followers_count))
            wait_clickable_click(browser, dict_xpaths['followers'])
            nap(5.6)
            if not browser.find_element('xpath', dict_xpaths['profile icon']).is_displayed:
                js_click_by_xpath(browser, dict_xpaths['followers'])
        elif unfollow:
            if not self.skip_followers:
                js_reload(browser)
            date_time_print('getting following')
            date_time_print('{} following count displayed'.format(self.displayed_following_count))
            wait_clickable_click(browser, dict_xpaths['following'])
            nap(5.6)
            if not browser.find_element('xpath', dict_xpaths['profile icon']).is_displayed:
                js_click_by_xpath(browser, dict_xpaths['following'])
        return

    def get_them(self, browser, unfollow=False):
        self.open_users(browser, unfollow)

        br = 19
        append_counter = 0
        append_users = True
        while self.current_len < self.displayed_rel_count:
            date_time_print(append_counter, append_users)
            if not unfollow:
                if append_counter > 3:
                    append_users = True
                    append_counter = 0
                else:
                    append_users = False
                    append_counter += 1
            self.loop_actions(browser, unfollow, append_users)
            date_time_print(self.current_len, self.displayed_rel_count)
            date_time_print(self.previous_len, self.current_len)
            last_scroll_counter = 0
            while (self.previous_len == self.current_len) and (last_scroll_counter < br):
                if last_scroll_counter == 0:
                    date_time_print('entered {} last loops'.format(br))
                self.loop_actions(browser, unfollow)
                last_scroll_counter += 1
            if last_scroll_counter >= br:
                break
        else:
            self.previous_len = -1
            self.current_len = 0
            self.displayed_rel_count = 0

        self.close_users(browser, unfollow)
        return

    def close_users(self, browser, unfollow):
        try:
            browser.find_element('xpath', dict_xpaths['close users windows']).click()
        except NoSuchElementException:
            date_time_print('***failed to get all followers, trying again***')
            self.get_them(browser, unfollow)
        if not unfollow:
            date_time_print('followers_list = ', len(self.followers_list))
            self.data['followers'] = self.followers_list
            self.save_data()
        if unfollow:
            date_time_print('following_list = ', len(self.following_list))
            self.data['following'] = self.followers_list
            self.save_data()
        nap(1.9)
        return

    def get_them_loop(self, browser, unfollow):
        if not unfollow:
            self.get_relation_count(browser, unfollow)
            while len(self.followers_list) < self.displayed_rel_count:
                self.get_them(browser, unfollow)

        elif unfollow:
            while len(self.unfollowing_list) > 0:
                self.get_them(browser, unfollow)
        return
