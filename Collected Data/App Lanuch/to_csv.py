import sys
import os
import csv
from collections import deque

sys.path.append(os.path.abspath('.'))
print(sys.path)

import android_time
import interpolate

def split_string_at_first_what(s):
	if s[0 : 5] == "https":
		first_space_index = s.find(' ')
	else:
		first_space_index = s.find('_')
	assert first_space_index != -1
	first_part = s[:first_space_index]
	second_part = s[first_space_index+1:]
	return first_part, second_part


# which, log_file, andr_file, data_file = "cmd5", "log", "andr", "data"
# which, log_file, andr_file, data_file = "cmd5", "log_2", "andr_2", "data_2"

# which, log_file, andr_file, data_file = "cmd10", "log", "andr", "data"
# which, log_file, andr_file, data_file = "cmd10", "log_2", "andr_2", "data_2"

# which, log_file, andr_file, data_file = "cmd15", "log", "andr", "data"
# which, log_file, andr_file, data_file = "cmd15", "log_2", "andr_2", "data_2"

# which, log_file, andr_file, data_file = "cpu5", "log", "andr", "data"
# which, log_file, andr_file, data_file = "cpu5", "log_2", "andr_2", "data_2"

# which, log_file, andr_file, data_file = "cpu10", "log10", "cpu10", "data"
# which, log_file, andr_file, data_file = "cpu10", "log10_2", "cpu10_2", "data_2"

# which, log_file, andr_file, data_file = "cpu15", "log15", "cpu15", "data"
# which, log_file, andr_file, data_file = "cpu15", "log15_2", "cpu15_2", "data_2"


# which, log_file, andr_file, data_file = "app_cmd5", "log", "andr", "data"
# which, log_file, andr_file, data_file = "app_cmd5", "log_2", "andr_2", "data_2"

# which, log_file, andr_file, data_file = "app_cmd10", "log", "andr", "data"
# which, log_file, andr_file, data_file = "app_cmd10", "log_2", "andr_2", "data_2"
# which, log_file, andr_file, data_file = "app_cmd10", "log_3", "andr_3", "data_3"

# which, log_file, andr_file, data_file = "app_cmd15", "log", "andr", "data"
# which, log_file, andr_file, data_file = "app_cmd15", "log_2", "andr_2", "data_2"
# which, log_file, andr_file, data_file = "app_cmd15", "log_testPriority", "andr_testPriority", "data_testPriority"
# which, log_file, andr_file, data_file = "app_cmd15", "log_testPriority2", "andr_testPriority2", "data_testPriority2"

# which, log_file, andr_file, data_file = "app_cpu5", "log", "andr", "data"
# which, log_file, andr_file, data_file = "app_cpu5", "log_2", "andr_2", "data_2"

# which, log_file, andr_file, data_file = "app_cpu10", "log", "andr", "data"
# which, log_file, andr_file, data_file = "app_cpu10", "log_2", "andr_2", "data_2"

# which, log_file, andr_file, data_file = "app_cpu15", "log", "andr", "data"
# which, log_file, andr_file, data_file = "app_cpu15", "log_2", "andr_2", "data_2"

# which, log_file, andr_file, data_file = "background_cpu10", "log", "andr", "data_afterinter"

old = 1 # is using interpolate

# which, log_file, andr_file, data_file = "app21_cpu10", "log", "andr", "data"
# which, log_file, andr_file, data_file = "honor_final_web21_cpu5", "log", "andr", "data"

which, log_file, andr_file, data_file = "honor_background_cpu5_2", "log", "andr", "data"

# working_in_folder_path = "process_data_pair/honor_compare_cpu"
working_in_folder_path = "process_data_pair/compare_multi_device_mode"
# working_in_folder_path = "process_data_pair/honor_final_app21_web21/honor_final_app21_cpu10"
# working_in_folder_path = "process_data_pair/honor_final_app21_web21/"

log_path = f"./{working_in_folder_path}/{which}/{log_file}.txt"
url_to_id_path = f"./{working_in_folder_path}/{which}/url_id.txt"
andr_path = f"./{working_in_folder_path}/{which}/{andr_file}.txt"

if old:
	data_path = f"./{working_in_folder_path}/{which}/{data_file}.csv"
else:
	data_path = f"./{working_in_folder_path}/{which}/{data_file}_afterinter.csv"



deque_pc = deque()
url_set = set()

with open(log_path, 'r') as f:
	''' read from pc.txt '''
	for i in f.readlines():

		i = i.strip()

		url, time_on_pc = split_string_at_first_what(i)
		url_set.add(url)

		# such as: https://www.google.com 2024-03-21 03:03:30+08:00, no microseconds
		if len(time_on_pc) == len("2024-03-21 03:03:30+08:00"):
			time_on_pc = time_on_pc[0:-6] + ".000000" + time_on_pc[-6:]
			
		assert len(time_on_pc) == len("2024-03-21 03:01:03.136000+08:00"), "len(time_on_pc)ERRORRRRRRR"

		micro_time = android_time.str1_to_microsecond(time_on_pc)
		deque_pc.append((micro_time, url))

print('len(deque_pc)', len(deque_pc), 'len(url_set)', len(url_set))

url_to_id = dict() 
for idx, url in enumerate(url_set):
	url_to_id[url] = idx

with open(url_to_id_path, 'a') as f:
	f.write(f"below is {which}\n")
	for i, j in url_to_id.items():
		f.write(f"{i} to {j}\n")

deque_android = deque()
with open(andr_path, 'r') as f:
	''' read from android's recording.txt '''
	for i in f.readlines():
		a, b, n0, n1, n2 = i.split()
		assert len(a) == len("2024-03-20") and len(b) == len("17:15:58.832")
		micro_time = android_time.str2_to_microsecond(a + " " + b)
		deque_android.append((micro_time, int(n0), int(n1), int(n2)))

print('len(deque_android)', len(deque_android))

microsecond_per_second = 1000000

if 1: # test_quality
	tiem_overflow_idxs = list() # overflow
	deque_android_temp = deque(deque_android)

	for idx, (tm, url) in enumerate(deque_pc): # shallow copy

		# [tl - 0.5s, tr + 5.45s)
		tl = tm - microsecond_per_second // 2
		tr = tm + int(microsecond_per_second * 5.45)

		inner_index = 0
		while deque_android_temp[0][0] < tr:
			t, *num = deque_android_temp.popleft()
			if t >= tl:
				if inner_index >= 600:
					print(tm, android_time.microseconds_to_str1(tm), inner_index, tl, tr, file=open("tiem_overflow.txt", 'a'))
				inner_index += 1

		if inner_index > 600:
			tiem_overflow_idxs.append(idx)

	print("tiem_overflow_num", len(tiem_overflow_idxs), "tiem_overflow_idxs", tiem_overflow_idxs)

# data_lsit: the array of length about 600
# labels_lsit: the label [0, 7) or [0, 21)
data_list, labels_list = [], []

for idx, (tm, url) in enumerate(deque_pc): 

	# time range: [tm - 0.5s, tm + 5.??s)
	# tl = tm - 0.5s
	# tr = tm + 5.??s
	data_tl_tr = [] # list[tuple[int, int, int, int]]

	tl = tm - microsecond_per_second // 2
	while deque_android[0][0] < tl:
		deque_android.popleft()

	tr = tm + int(microsecond_per_second * 5.65)
	while deque_android[0][0] < tr:
		data_tl_tr.append(deque_android.popleft()) 

	if old:
		data_tl_tr = interpolate.no_interpolate(data_tl_tr)
	else:
		data_tl_tr = interpolate.interpolate(data_tl_tr, data_tl_tr[0][0])

	if len(data_tl_tr) > 600:
		data_tl_tr = data_tl_tr[0 : 600]
	if len(data_tl_tr) < 600:
		data_tl_tr += [[0.0, 0.0, 0.0] for _ in range(600 - len(data_tl_tr))]
	
	assert len(data_tl_tr[0]) == 3

	data_flat = []
	for i in range(3):
		data_flat += [one_row[i] for one_row in data_tl_tr]
	
	data_list.append(data_flat)
	labels_list.append(url_to_id[url])

assert len(data_list[0]) == 600 * 3

with open(data_path, 'w', newline='') as file:
	writer = csv.writer(file)
	
	header = ['feature_' + str(i) for i in range(1, 1801)] + ['label']
	writer.writerow(header)
	
	for data, label in zip(data_list, labels_list):
		row = list(data) + [label]
		writer.writerow(row)




# deque_pc = deque()
# url_set = set()
# with open(log_path, 'r') as f:
# 	'''
# 		read from pc.txt
# 	'''
# 	for i in f.readlines():

# 		i = i.strip()
# 		if len(i) == 0 or i[0] == 'x':
# 			continue

# 		url, time_on_pc = split_string_at_first_what(i)
# 		url_set.add(url)

# 		# such as: https://www.google.com 2024-03-21 03:03:30+08:00, no microseconds
# 		if len(time_on_pc) == len("2024-03-21 03:03:30+08:00"):
# 			time_on_pc = time_on_pc[0:-6] + ".000000" + time_on_pc[-6:]
			
# 		if not len(time_on_pc) == len("2024-03-21 03:01:03.136000+08:00"):
# 			print(time_on_pc)
# 			assert(0)

# 		micro_time = android_time.str1_to_microsecond(time_on_pc)
# 		deque_pc.append((micro_time, url))

# print('len(deque_pc)', len(deque_pc))
# print('len(url_set)', len(url_set))

# url_to_id = dict() 
# for idx, url in enumerate(url_set):
# 	url_to_id[url] = idx

# with open(url_to_id_path, 'a') as f:
# 	f.write(f"below is {which}\n")
# 	for i, j in url_to_id.items():
# 		f.write(f"{i} to {j}\n")

# deque_android = deque()
# with open(andr_path, 'r') as f:
# 	'''
# 		read from android's recording.txt
# 	'''
# 	for i in f.readlines():
# 		a, b, n0, n1, n2 = i.split()
# 		assert len(a) == len("2024-03-20") and len(b) == len("17:15:58.832")
# 		micro_time = android_time.str2_to_microsecond(a + " " + b)
# 		deque_android.append((micro_time, int(n0), int(n1), int(n2)))

# print('len(deque_android)', len(deque_android))

# microsecond_per_second = 1000000

# test_quality = 1
# if test_quality:
# 	tiem_overflow_idxs = list() # overflow
# 	deque_android_temp = deque(deque_android)

# 	for idx, (tm, url) in enumerate(deque_pc): # shallow copy

# 		# [tl - 0.5s, tr + 5.45s)
# 		tl = tm - microsecond_per_second // 2
# 		tr = tm + int(microsecond_per_second * 5.45)

# 		inner_index = 0
# 		while deque_android_temp[0][0] < tr:
# 			t, *num = deque_android_temp.popleft()
# 			if t >= tl:
# 				if inner_index >= 600:
# 					print(tm, android_time.microseconds_to_str1(tm), inner_index, tl, tr, file=open("tiem_overflow.txt", 'a'))
# 				inner_index += 1

# 		if inner_index > 600:
# 			tiem_overflow_idxs.append(idx)

# 	print("tiem_overflow_num", len(tiem_overflow_idxs))
# 	print("tiem_overflow_idxs", tiem_overflow_idxs)


# # data_lsit: the array of length about 600
# # labels_lsit: the label [0, 7) or [0, 21)
# data_list, labels_list = [], []

# # overflow's record
# tiem_overflow = set() 

# for idx, (tm, url) in enumerate(deque_pc): 

# 	# time range: [tm - 0.5s, tm + 5.??s)
# 	# tl = tm - 0.5s
# 	# tr = tm + 5.??s
# 	data_tl_tr = [] # list[tuple[int, int, int, int]]

# 	tl = tm - microsecond_per_second // 2
# 	while deque_android[0][0] < tl:
# 		deque_android.popleft()

# 	tr = tm + int(microsecond_per_second * 5.65)
# 	while deque_android[0][0] < tr:
# 		data_tl_tr.append(deque_android.popleft()) 
	
# 	if not old:
# 		data_tl_tr = interpolate.interpolate(data_tl_tr, tl)

# 	if len(data_tl_tr) > 600:
# 		data_tl_tr = data_tl_tr[0 : 600]
# 	if len(data_tl_tr) < 600:
# 		data_tl_tr += [[0.0, 0.0, 0.0] for _ in range(600 - len(data_tl_tr))]
	
# 	data_flat = []
# 	for i in range(3):
# 		data_flat += [j[i] for j in data_tl_tr]
	
# 	data_list.append(data_flat)
# 	labels_list.append(url_to_id[url])


# with open(data_path, 'w', newline='') as file:
# 	writer = csv.writer(file)
	
# 	header = ['feature_' + str(i) for i in range(1, 1801)] + ['label']
# 	writer.writerow(header)
	
# 	for data, label in zip(data_list, labels_list):
# 		row = list(data) + [label]
# 		writer.writerow(row)
