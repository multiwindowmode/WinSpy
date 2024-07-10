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

def get_current_time():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

def split_string_at_first_what(s):
	first_space_index = s.find(' ')
	assert first_space_index != -1
	first_part = s[ : first_space_index]
	second_part = s[first_space_index + 1 : ]
	return first_part, second_part

folder_path = os.path.join(".", "inner_app_data", "inner_app_chat_background")
# folder_path = os.path.join(".", "inner_app_data", "inner_app_chat_res")
log_path = os.path.join(folder_path, "log.txt")
andr_path = os.path.join(folder_path, "andr.txt")

deque_pc = deque()

with open(log_path, 'r') as f:
	''' read from pc's record '''
	for i in f.readlines():
		i = i.strip()
		operation_type, time_on_pc = split_string_at_first_what(i)

		# such as: CameraSwipeAt 2024-03-21 03:03:30+08:00, no microseconds
		if len(time_on_pc) == len("2024-03-21 03:03:30+08:00"):
			time_on_pc = time_on_pc[0:-6] + ".000000" + time_on_pc[-6:]
		assert len(time_on_pc) == len("2024-03-21 03:01:03.136000+08:00"), "len(time_on_pc) Error"

		micro_time = android_time.str1_to_microsecond(time_on_pc)
		deque_pc.append((micro_time, operation_type))

print('len(deque_pc)', len(deque_pc), get_current_time())

list_android = list()
with open(andr_path, 'r') as f:
	''' read from android's record '''
	for i in f.readlines():
		a, b, n0, n1, n2 = i.split()
		assert len(a) == len("2024-03-20") and len(b) == len("17:15:58.832")
		micro_time = android_time.str2_to_microsecond(a + " " + b)
		list_android.append((micro_time, int(n0), int(n1), int(n2)))

print('len(deque_android)', len(list_android), get_current_time())

def index_to_insert_t0(list_of_tuples, x) -> int:
    def extract_first(t):
        return t[0]
    return bisect_left(list_of_tuples, x, key=extract_first)

microsecond_per_second = 1000000

def get_cpu_of_index_range(il, ir): # from list_android
	res = []
	for (tm, n0, n1, n2) in list_android[il : ir]:
		res.append(n0)
	return res

def do_resize(a, new_size):
	b = a + [0] * new_size
	return b[0 : new_size]

data_path = os.path.join(folder_path, f"data_by_random_selection.csv")

# data_lsit: the array of length time_len
# labels_lsit: the label 0/1
data_list, labels_list = [], []
# index_range_list = [] # to judge the intersection

time_len = 4

# for (ope, time_len) in [("VoiceSwipeAt", 3), ("CameraSwipeAt", 3), ("MsgBoxClickAt", 3)]:
# 	index_len = time_len * 100 # the length of index range
# 	for idx, (tm, operation_type) in enumerate(deque_pc): 
# 		# time range: [tm - 0.01s, tm + after_time + 0.01)
# 		if operation_type == ope:
# 			tl = tm - microsecond_per_second * 0.01
# 			tr = tm + int(microsecond_per_second * (after_time + 0.05))
# 			tl_index = index_to_insert_t0(list_android, tl)
# 			tr_index = index_to_insert_t0(list_android, tr)
# 			index_range_list.append((tl_index, tr_index))

for (ope, time_len) in [("VoiceSwipeAt", 4), ("CameraSwipeAt", 4), ("MsgBoxClickAt", 4)]:
	index_len = time_len * 100 # the length of index range

for idx, (tm, operation_type) in enumerate(deque_pc): 
	# time range: [tm - 0.05s, tm + time_len + 0.05)

	for _ in range(4):
		random_before = random.uniform(0.5, 1.5)
		tl = tm - int(microsecond_per_second * random_before)
		tr = tm + int(microsecond_per_second * (time_len + 0.01))
		tl_index = index_to_insert_t0(list_android, tl)
		tr_index = index_to_insert_t0(list_android, tr)
		data_now = get_cpu_of_index_range(tl_index, tr_index)
		data_list.append(do_resize(data_now, index_len))

		if operation_type in ["VoiceSwipeAt", "CameraSwipeAt", "MsgBoxClickAt"]:
			labels_list.append(operation_type)
		else:
			labels_list.append("other")

print(len(data_list), len(labels_list), get_current_time())
print(len(data_list[0]))
	
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

# ope_num = len(labels_list)
# for _ in range(ope_num * 1):
# 	while 1:
# 		min_index = 0
# 		max_index = len(list_android) - index_len

# 		idx_st = random.randint(min_index, max_index)
# 		idx_ed = idx_st + index_len

# 		if not judge_intersection(idx_st, idx_ed):
# 			data_now = get_cpu_of_index_range(idx_st, idx_ed)
# 			data_list.append(do_resize(data_now, index_len))
# 			labels_list.append("other")
# 			break

# 	assert len(data_list[0]) == index_len

to_write = list(zip(data_list, labels_list))
random.shuffle(to_write)

with open(data_path, 'w', newline='') as file:
	writer = csv.writer(file)
	
	header = ['feature_' + str(i + 1) for i in range(len(data_list[0]))] + ['label']
	writer.writerow(header)

	cnt = {}
	for data, label in to_write:
		if label not in cnt:
			cnt[label] = 0
		cnt[label] += 1

		row = list(data) + [label]
		writer.writerow(row)

	print(cnt)