
apk_packages = '''org.telegram.messenger
com.instagram.android
jp.pxv.android
com.tinder
com.google.android.gm
com.google.android.apps.translate
com.facebook.katana
com.google.android.youtube
com.whatsapp
com.netflix.mediaclient
com.facebook.orca
com.spotify.music
com.zhiliaoapp.musically
com.tencent.mm
com.microsoft.emmx
org.mozilla.firefox
tv.danmaku.bili
com.google.android.apps.maps
com.android.chrome
jp.naver.line.android
com.valvesoftware.android.steam.community
'''
# adb shell pm list packages -f: list all the app and its package name


import os
import sys
import random
print(os.getcwd())

sys.path.append(os.path.abspath('.'))

import android_time
import ope_funcs
import time

point_left_top = (195, 272)
point_left_bottom = (195, 1740)
point_right_top = (925, 272)
honor_device_id = "AVNS023926003923"

# def log_time(s1):
#     with open("open_app/oa_log.txt", "a") as f:
#         f.write(s1 + "\n")

home_pos = (1083, 2311)
back_pos = (606, 2284)
def tap_home_back(n_home, n_back):
    for _ in range(n_home):
        ope_funcs.tap_xy(honor_device_id, *home_pos)
        time.sleep(0.1)

    for _ in range(n_back):
        ope_funcs.tap_xy(honor_device_id, *back_pos)
        time.sleep(0.1)

def go():
    '''
    for1
        for2
            check < 21
                log_begin_time
                tap
                10s
                close
                1s
    '''
    while 1:

        if not ope_funcs.check_screen_on(honor_device_id):
            ope_funcs.log(f"screen_off_at_{android_time.get_android_time(honor_device_id)}", "open_app/oa_log.txt")
            break

        if not ope_funcs.check_battery_level(honor_device_id):
            ope_funcs.log(f"low_battery_at_{android_time.get_android_time(honor_device_id)}", "open_app/log.txt")
            break

        w = random.randint(0, 3)
        h = random.randint(0, 5)

        idx = w * 6 + h

        # if idx < 7:

        if idx < 21:

            px = int((point_right_top[0] - point_left_top[0]) / 3 * w + point_left_top[0])
            py = int((point_left_bottom[1] - point_left_top[1]) / 5 * h + point_left_top[1])

            package_name = apk_packages.split()[idx]

            ope_funcs.log(f"{package_name}_{android_time.get_android_time(honor_device_id)}", "open_app/oa_log.txt")

            ope_funcs.tap_xy(honor_device_id, px, py)
            ope_funcs.tap_xy(honor_device_id, px, py)

            time.sleep(10.0)
            
            ope_funcs.force_stop_app(honor_device_id, package_name)
            ope_funcs.kill_app(honor_device_id, package_name)

            # three times upward stroke
            tap_home_back(3, 2)

            ope_funcs.force_stop_app(honor_device_id, package_name)
            ope_funcs.kill_app(honor_device_id, package_name)

            # three times left-right stroke
            tap_home_back(3, 2)

            time.sleep(0.2)

            time.sleep(2.0)


if __name__ == "__main__":
    go()