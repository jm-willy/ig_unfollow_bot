from user_config import my_username

window_class_name = '_aano'

dict_xpaths = {
    'profile icon': '//*[@href="/{}/"]'.format(my_username),
    'followers': '//*[text()=" followers"]//parent::a',
    'following': '//*[text()=" following"]//parent::a',
    'followers count': '//*[text()=" followers"]//span/span',
    'following count': '//*[text()=" following"]//span/span',
    'users relation window': '//*[@class="{}"]'.format(window_class_name),
    'usernames': '//*[@class="{}"]/div/div/div/div[2]//*[@href]'.format(window_class_name),
    'user following unfollow button': '//*[text()="{}"]//ancestor::*[@role="button"]//button',
    'user following confirm unfollow button': '//button[text()="Unfollow"]',
    'close users windows': '//*[@class="_aano"]//parent::div//*[@class="_abl-"]',
},
