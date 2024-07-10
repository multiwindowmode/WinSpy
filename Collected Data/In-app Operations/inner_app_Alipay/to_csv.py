import sys
import os
import csv
from collections import deque
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime
from bisect import bisect_left
import random

sys.path.append(os.path.abspath('.'))
print(sys.path)

import android_time
import interpolate
import process_data_pair.honor_compare_cpu.train_func as tf



# folder_path = os.path.join(".", "inner_app_data", "inner_app_pay_res")
folder_path = os.path.join(".", "inner_app_data", "inner_app_pay_background")
log_path = os.path.join(folder_path, "log.txt")
andr_path = os.path.join(folder_path, "andr.txt")



'''
time, ope_type
time, ope_type
time, ope_type
time, ope_type
'''
deque_pc = deque()
with open(log_path, 'r') as f:
	''' read from pc's record '''
	for i in f.readlines():
		i = i.strip()

		def split_string_at_first_what(s): # 'abc def' -> ('abc', 'def')
			first_space_index = s.find(' ')
			assert first_space_index != -1
			first_part = s[ : first_space_index]
			second_part = s[first_space_index + 1 : ]
			return first_part, second_part
		operation_type, time_on_pc = split_string_at_first_what(i)

		# such as: CameraSwipeAt 2024-03-21 03:03:30+08:00, no microseconds
		if len(time_on_pc) == len("2024-03-21 03:03:30+08:00"):
			time_on_pc = time_on_pc[0:-6] + ".000000" + time_on_pc[-6:]
		assert len(time_on_pc) == len("2024-03-21 03:01:03.136000+08:00"), "len(time_on_pc) Error"

		micro_time = android_time.str1_to_microsecond(time_on_pc)
		deque_pc.append((micro_time, operation_type))
print('len(deque_pc)', len(deque_pc))





'''
time n0 n1 n2
time n0 n1 n2
time n0 n1 n2
'''
list_android = list()
with open(andr_path, 'r') as f:
	''' read from android's record '''
	for i in f.readlines():
		a, b, n0, n1, n2 = i.split()
		assert len(a) == len("2024-03-20") and len(b) == len("17:15:58.832")
		micro_time = android_time.str2_to_microsecond(a + " " + b)
		list_android.append((micro_time, int(n0), int(n1), int(n2)))

print('len(deque_android)', len(list_android))







def index_to_insert_t0(list_of_tuples, x) -> int:
    def extract_first(t):
        return t[0]
    return bisect_left(list_of_tuples, x, key=extract_first)

def get_cpu_of_index_range(il, ir): # from list_android
	res = []
	for (tm, n0, n1, n2) in list_android[il : ir]:
		res.append(n0)
	return res

def do_resize(a, new_size):
	b = a + [0] * new_size
	return b[0 : new_size]


microsecond_per_second = 1000000
# for (ope, time_len) in [("tapConfirmWithdrawalAt", 3), ("tapConfirmRechargeAt", 3)]:
if 1:
	time_len = 4
	index_len = time_len * 100

	# data_path = os.path.join(folder_path, f"data_{ope}.csv")
	data_path = os.path.join(folder_path, f"data.csv")

	# data_list: the list of array of length time_len
	# labels_list: the label 0/1
	data_list, labels_list = [], []

	index_range_list = []
	# for idx, (tm, operation_type) in enumerate(deque_pc): 
	# 	# time range: [tm - random, tm + time_len + 0.05)
	# 	if operation_type == "tapConfirmWithdrawalAt" or operation_type == "tapConfirmRechargeAt":
	# 		tl = tm - microsecond_per_second * 0.01
	# 		tr = tm + int(microsecond_per_second * (time_len + 0.05))
	# 		tl_index = index_to_insert_t0(list_android, tl)
	# 		tr_index = index_to_insert_t0(list_android, tr)

	# 		data_now = get_cpu_of_index_range(tl_index, tr_index)
	# 		data_list.append(do_resize(data_now, index_len))
	# 		labels_list.append(1)

	# 		index_range_list.append((tl_index, tr_index))

	for idx, (tm, operation_type) in enumerate(deque_pc): 
		# time range: [tm - random, tm + time_len + 0.05)

		random_before = random.uniform(0.5, 1.5)
		tl = tm - microsecond_per_second * random_before
		tr = tm + int(microsecond_per_second * (time_len + 0.05))
		tl_index = index_to_insert_t0(list_android, tl)
		tr_index = index_to_insert_t0(list_android, tr)

		data_now = get_cpu_of_index_range(tl_index, tr_index)
		data_list.append(do_resize(data_now, index_len))
		if operation_type == "tapConfirmWithdrawalAt" or operation_type == "tapConfirmRechargeAt":
			labels_list.append(operation_type)
			index_range_list.append((tl_index, tr_index))
		else:
			labels_list.append('other')

	# def judge_intersection(l, r):
	# 	i = bisect_left(index_range_list, (l, r))
	# 	for j in range(i - 2, i + 3):
	# 		if j >= 0 and j < len(index_range_list):
	# 			lj, rj = index_range_list[j]
	# 			if r <= lj or l >= rj:
	# 				pass
	# 			else:
	# 				return True
	# 	return False

	# for _ in range(0):
	# 	while 1:
	# 		min_index = 0
	# 		max_index = len(list_android) - index_len

	# 		idx_st = random.randint(min_index, max_index)
	# 		idx_ed = idx_st + index_len

	# 		if not judge_intersection(idx_st, idx_ed):
	# 			data_now = get_cpu_of_index_range(idx_st, idx_ed)
	# 			data_list.append(do_resize(data_now, index_len))
	# 			labels_list.append(0)
	# 			break
	
	print(len(data_list), len(labels_list), len(data_list[0]))
	assert len(data_list[0]) == index_len

	to_write = list(zip(data_list, labels_list))

	with open(data_path, 'w', newline='') as file:
		writer = csv.writer(file)
		
		header = ['feature_' + str(i + 1) for i in range(len(data_list[0]))] + ['label']
		writer.writerow(header)

		n0, n1 = 0, 0
		for data, label in to_write:
			if label == 0:
				n0 += 1
			else:
				n1 += 1
			row = list(data) + [label]
			writer.writerow(row)