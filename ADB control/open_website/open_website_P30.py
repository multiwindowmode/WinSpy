import time
import os
import sys
import random

sys.path.append(os.path.abspath('.'))

import android_time
from ope_funcs import *


urls = []
urls.append("https://www.google.com")
urls.append("https://www.instagram.com")
urls.append("https://m.facebook.com")
urls.append("https://www.twitter.com")
urls.append("https://m.baidu.com")
urls.append("https://m.youtube.com")
urls.append("https://www.netflix.com")
urls.append("https://m.bilibili.com")
urls.append("https://www.amazon.com")
urls.append("https://www.ebay.com")
urls.append("https://www.paypal.com")
urls.append("https://m.twitch.tv")
urls.append("https://www.indeed.com")
urls.append("https://www.wikipedia.org")
urls.append("https://www.quora.com")
urls.append("https://maps.google.com")
urls.append("https://www.deepl.com")
urls.append("https://www.yahoo.com")
urls.append("https://www.weather.com")
urls.append("https://www.espn.com")
urls.append("https://www.booking.com")

device_ids = []
device_ids.append("AVNS023926003923")
device_ids.append("8KE5T19515023226")

'''
    step1: open browser
    step2: wait for browser's init, that is, open a black web
    step3: record the timestamp as the begin time
    step4: send intent for the target, wait for 3s
    step5: stop the browser
'''
def steps1():
    sel = 0

    browser_package_name = "com.microsoft.emmx"
    blank_page_url = "https://www.example.com"

    random_index = -1

    while True:
        # random_index = random.randint(0, len(urls) - 1)

        random_index += 1
        random_index %= len(urls)

        url = urls[random_index]

        open_url_with_browser(device_ids[sel], blank_page_url, browser_package_name)

        time.sleep(0.5)

        open_url_with_browser(device_ids[sel], blank_page_url, browser_package_name)

        time.sleep(2.0)
        
        current_time_on_device = android_time.get_android_time(device_ids[sel])
        log(f'{url} {current_time_on_device}')

        open_url_with_browser(device_ids[sel], url, browser_package_name)

        time.sleep(7.0)

        force_stop_app(device_ids[sel], browser_package_name)

        time.sleep(0.5)

        force_stop_app(device_ids[sel], browser_package_name)



'''
    step1: make sure the explorer opened
    step2: repeat twice
        step21: tap the input box
        step22: backspace * 30
    step4: url input
    step5: input enter after the log the time point
    step6: wait 7s
'''
def steps2():
    sel = 1
    # pos = (730, 170) 
    pos = (670, 180)

    random_index = -1

    while True:

        if not check_screen_on(device_ids[sel]):
            log(f"screen_off_at_{android_time.get_android_time(device_ids[sel])}", "open_website/log.txt")
            break

        if not check_battery_level(device_ids[sel]):
            log(f"low_battery_at_{android_time.get_android_time(device_ids[sel])}", "open_website/log.txt")
            break

        send_swipe(device_ids[sel], (600, 1200), (600, 1400), 500)

        # random_index += 1
        # random_index %= len(urls)
        # random_index = random.randint(0, len(urls) - 1)
        random_index = random.randint(0, 6)

        url = urls[random_index]

        for _ in range(2):
            time.sleep(0.5)
            tap_xy(device_ids[sel], pos[0], pos[1])
            send_delete(device_ids[sel], 30)

        send_string(device_ids[sel], url)

        time.sleep(0.1)
        
        log(f'{url} {android_time.get_android_time(device_ids[sel])}', "open_website/log.txt")

        send_enter(device_ids[sel])

        time.sleep(7.0)


if __name__ == "__main__":
    steps2()