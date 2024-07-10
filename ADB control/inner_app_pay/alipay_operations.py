import os
import sys
import random
print(os.getcwd())

sys.path.append(os.path.abspath('.'))

import android_time
import ope_funcs
import time

# steps:
# click back * 10
# click alipy 
# click blance
# branch1: tap details -> random click top 3 -> random click detail
# branch2: withdraw/recharge -> 0.01 -> confirm -> back * 2 -> 0.01 -> ...

honor_device_id = "AVNS023926003923"

def tap_back_n(n, interval = 0.15):
	pos_back = (313, 2315)
	for _ in range(n):
		ope_funcs.tap_xy(honor_device_id, *pos_back)
		time.sleep(interval)

def at_begining():
	tap_back_n(5)
	time.sleep(0.5)
	tap_back_n(5)

	pos_alipay = (898, 1702)
	pos_bottom_me = (937, 2173)
	pos_balance = (500, 1366)

	ope_funcs.log(f"tapBeginsAt {android_time.get_android_time(honor_device_id)}", "inner_app_pay/log.txt")
	ope_funcs.tap_xy(honor_device_id, *pos_alipay)
	time.sleep(5)
	ope_funcs.tap_xy(honor_device_id, *pos_bottom_me)
	time.sleep(4)
	ope_funcs.tap_xy(honor_device_id, *pos_balance)
	time.sleep(5)
	


def tap_0_01():
	pos_input = (366, 850)
	for _ in range(3):
		ope_funcs.tap_xy(honor_device_id, *pos_input)
		time.sleep(0.2)

	time.sleep(1)

	pos_zero = (279, 2188)
	pos_point = (679, 2173)
	pos_one = (149, 1680)
	for p in [pos_zero, pos_point, pos_zero, pos_one]:
		ope_funcs.tap_xy(honor_device_id, *p)
		time.sleep(1)
	time.sleep(5)

def tap_withdrawal():
	pos_with = (302, 884)
	time.sleep(1)
	ope_funcs.log(f"tapWithdrawalPageAt {android_time.get_android_time(honor_device_id)}", "inner_app_pay/log.txt")
	ope_funcs.tap_xy(honor_device_id, *pos_with)
	time.sleep(5)
	tap_0_01()
	pos_confirm = (914, 2005)
	for _ in range(3):
		ope_funcs.log(f"tapConfirmWithdrawalAt {android_time.get_android_time(honor_device_id)}", "inner_app_pay/log.txt")
		ope_funcs.tap_xy(honor_device_id, *pos_confirm)
		time.sleep(5)
		tap_back_n(2, interval = 2.0)
		time.sleep(5)
		
def tap_recharge():
	pos_rech = (796, 872)
	ope_funcs.log(f"tapRechargePageAt {android_time.get_android_time(honor_device_id)}", "inner_app_pay/log.txt")
	ope_funcs.tap_xy(honor_device_id, *pos_rech)
	time.sleep(5)
	tap_0_01()
	time.sleep(1)
	pos_confirm = (914, 2005)	
	for _ in range(3):
		ope_funcs.log(f"tapConfirmRechargeAt {android_time.get_android_time(honor_device_id)}", "inner_app_pay/log.txt")
		ope_funcs.tap_xy(honor_device_id, *pos_confirm)
		time.sleep(5)
		tap_back_n(2, interval = 1.0)
		time.sleep(5)

def tap_detail_all():
	pos_detail_all = (936, 1087)
	ope_funcs.log(f"tapDetailAllAt {android_time.get_android_time(honor_device_id)}", "inner_app_pay/log.txt")
	ope_funcs.tap_xy(honor_device_id, *pos_detail_all)
	time.sleep(5)

def random_click_top():
	pos_top_left = (191, 283)
	pos_top_mid = (540, 283)
	pos_top_right = (886, 283)
	poss = [pos_top_left, pos_top_mid, pos_top_right]
	which = random.randint(0, 2)

	ope_funcs.log(f"tapRandomTopAt {android_time.get_android_time(honor_device_id)}", "inner_app_pay/log.txt")
	ope_funcs.tap_xy(honor_device_id, *poss[which])
	time.sleep(5)

def random_item():
	pos_list_top = (585, 500)
	pos_list_bottom = (585, 1631)
	pos_list_len = 7

	dy = (pos_list_bottom[1] - pos_list_top[1]) / (pos_list_len - 1)
	
	for _ in range(7):
		idx = random.randint(0, pos_list_len - 1)
		pos_idx = (pos_list_top[0], pos_list_top[1] + dy * idx)
		ope_funcs.log(f"tapRandomItemAt {android_time.get_android_time(honor_device_id)}", "inner_app_pay/log.txt")
		ope_funcs.tap_xy(honor_device_id, *pos_idx)
		time.sleep(5)
		tap_back_n(1)
		time.sleep(5)
		
for o in range(int(1e100)):

	if not ope_funcs.check_screen_on(honor_device_id):
		ope_funcs.log(f"screen_off_at_{android_time.get_android_time(honor_device_id)}", "inner_app_pay/log.txt")
		break

	if not ope_funcs.check_battery_level(honor_device_id):
		ope_funcs.log(f"low_battery_at_{android_time.get_android_time(honor_device_id)}", "inner_app_pay/log.txt")
		break

	at_begining()
	time.sleep(2)
	if o % 3 == 0:
		tap_withdrawal()
	elif o % 3 == 1:
		tap_recharge()
	else:
		tap_detail_all()
		random_item()
	