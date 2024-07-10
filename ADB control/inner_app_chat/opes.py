import os
import sys
import random
print(os.getcwd())

sys.path.append(os.path.abspath('.'))

import android_time
import ope_funcs
import time

def get_pos_bottom():
    pos_chats_x = 140
    pos_calls_x = 933
    pos_bottom_y = 2125
    pos_bottom = []
    for i in range(4):
        dx = (pos_calls_x - pos_chats_x ) / 3
        pos_bottom.append((int(pos_chats_x + dx * i), pos_bottom_y))
    return pos_bottom


def tap_back_n(n_back):
    for _ in range(n_back):
        ope_funcs.tap_xy(honor_device_id, *pos_back)
        time.sleep(0.2)

def click_whatsapp():
    ope_funcs.tap_xy(honor_device_id, *pos_whatsapp)

def bottom_random_n(n_times):
    whichs = [random.randint(1, 3)]
    for _ in range(n_times):
        while 1:
            cur = random.randint(0, 3)
            if cur != whichs[-1]:
                whichs.append(cur)
                break
    if whichs[-1] != 0:
        whichs.append(0)
    for which in whichs:
        p = get_pos_bottom()[which]
        ope_funcs.log(f"BottomClick{which}At {android_time.get_android_time(honor_device_id)}", "inner_app_chat/log.txt")
        ope_funcs.tap_xy(honor_device_id, *p)
        time.sleep(2)

def click_chat():
    ope_funcs.log(f"ClickChatAt {android_time.get_android_time(honor_device_id)}", "inner_app_chat/log.txt")
    ope_funcs.tap_xy(honor_device_id, *pos_the_first_chat)
    time.sleep(2)

def voice_swipe(n_times):
    for _ in range(n_times):
        ope_funcs.log(f"VoiceSwipeAt {android_time.get_android_time(honor_device_id)}", "inner_app_chat/log.txt")
        ope_funcs.send_swipe(honor_device_id, pos_voice_from, pos_voice_to, 4000)
        time.sleep(2)

def camera_swipe_n(n_times):
    for _ in range(n_times):
        ope_funcs.log(f"CameraSwipeAt {android_time.get_android_time(honor_device_id)}", "inner_app_chat/log.txt")
        ope_funcs.send_swipe(honor_device_id, pos_camera_from, pos_camera_to, 4000)
        time.sleep(2)

def message_box_click():
    for ps in [pos_msg_box_emoji, pos_msg_box] * 2:
        ope_funcs.log(f"MsgBoxClickAt {android_time.get_android_time(honor_device_id)}", "inner_app_chat/log.txt")
        ope_funcs.tap_xy(honor_device_id, *ps)
        time.sleep(2)
        ope_funcs.tap_xy(honor_device_id, *pos_back)
        time.sleep(1)

# steps:
# make sure the vpn is open
# open the spy app in float window
# do opes

honor_device_id = "AVNS023926003923"
pos_whatsapp = (420, 840)
pos_back = (325, 2318) # the pos of back in part screen
pos_the_first_chat = (540, 400)
pos_voice_from = (997, 2168)
pos_voice_to = (440, 2168)
pos_camera_from = (822, 2185)
pos_camera_to = (360, 2185)
pos_msg_box_emoji = (86, 2180)
pos_msg_box = (240, 2177)

while 1:
    if not ope_funcs.check_screen_on(honor_device_id):
        ope_funcs.log(f"screen_off_at_{android_time.get_android_time(honor_device_id)}", "inner_app_chat/log.txt")
        break

    if not ope_funcs.check_battery_level(honor_device_id):
        ope_funcs.log(f"low_battery_at_{android_time.get_android_time(honor_device_id)}", "inner_app_chat/log.txt")
        break

    tap_back_n(7)
    click_whatsapp()
    time.sleep(3)
    bottom_random_n(7)
    click_chat()
    voice_swipe(2)
    time.sleep(2)
    camera_swipe_n(2)
    time.sleep(2)
    message_box_click()
    tap_back_n(7)