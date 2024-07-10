import sys
import os
import csv
from collections import deque
from concurrent.futures import ProcessPoolExecutor

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

# which = "./process_data_pair/honor_final_app21_web21/honor_final_app21_cpu10/app21_cpu10_4"
# which = "./process_data_pair/honor_final_app21_web21/honor_final_app21_cpu10/app21_cpu10_merge12345"
# which = "./process_data_pair/honor_final_app21_web21/honor_final_app21_cpu10/app21_cpu10_without_netacc"
# which = "./process_data_pair/honor_final_app21_web21/honor_final_app21_cpu10/app21_cpu10_foreach"
which = "./process_data_pair/honor_final_app21_web21/honor_final_app21_cpu10/app21_cpu10_foreach2"
# which = "./process_data_pair/honor_final_app21_web21/honor_final_background_app21/"
# which = "./process_data_pair/honor_final_app21_web21/honor_final_background_web21/"
# which = "./process_data_pair/honor_final_app21_web21/honor_final_web21_cpu5"
# which = "./process_data_pair/honor_compare_cpu/app_cmd10"
# which = "./process_data_pair/honor_compare_cpu/app_cpu10"
# which = "./process_data_pair/compare_multi_device_mode/honor_background_cpu5"
# which = "./process_data_pair/compare_multi_device_mode/honor_background_cpu5"
# which = "./process_data_pair/compare_multi_device_mode/P30_background_cpu5"
# which = "./process_data_pair/compare_multi_device_mode/honor_large_app7_web7/honor_large_web7_cpu5"

log_path = f"{which}/log.txt"
andr_path = f"{which}/andr.txt"
data_path = f"{which}/data.csv"
url_id_path = f"{which}/url_id.txt"

deque_pc = deque()
url_set = set()
with open(log_path, 'r') as f: # pc's log
	idx = 0
	for i in f.readlines():
		idx += 1
		i = i.strip()
		url, time_on_pc = split_string_at_first_what(i)
		url_set.add(url)
		# such as: https://www.google.com 2024-03-21 03:03:30+08:00, no microseconds
		if len(time_on_pc) == len("2024-03-21 03:03:30+08:00"):
			time_on_pc = time_on_pc[0:-6] + ".000000" + time_on_pc[-6:]
		
		if not len(time_on_pc) == len("2024-03-21 03:01:03.136000+08:00"):
			print(len(time_on_pc), idx)

		assert len(time_on_pc) == len("2024-03-21 03:01:03.136000+08:00"), "len(time_on_pc) error"
		micro_time = android_time.str1_to_microsecond(time_on_pc)
		deque_pc.append((micro_time, url))

print('len(deque_pc)', len(deque_pc), 'len(url_set)', len(url_set))

url_to_id = dict() 
for idx, url in enumerate(url_set):
	url_to_id[url] = idx

with open(url_id_path, 'a') as f:
	for i, j in url_to_id.items():
		print(i, "to", j, file=f)

deque_android = deque()
with open(andr_path, 'r') as f: # from android's recording.txt
	for i in f.readlines():
		a, b, n0, n1, n2 = i.split()
		assert len(a) == len("2024-03-20") and len(b) == len("17:15:58.832")
		micro_time = android_time.str2_to_microsecond(a + " " + b)
		deque_android.append((micro_time, int(n0), int(n1), int(n2)))
		
print('len(deque_android)', len(deque_android))

microsecond_per_second = 1000000
# data_lsit: the array of length about 600
# labels_lsit: the label [0, 7) or [0, 21)
data_list, labels_list = [], []

for idx, (tm, url) in enumerate(deque_pc): 
	# time range: [tm - 0.5s, tm + 5.??s)
	data_tl_tr = [] # list[tuple[int, int, int, int]]

	tl = tm - microsecond_per_second // 2
	while deque_android[0][0] < tl:
		deque_android.popleft()
	tr = tm + int(microsecond_per_second * 5.65)
	while deque_android[0][0] < tr:
		data_tl_tr.append(deque_android.popleft()) 

	data_tl_tr = interpolate.no_interpolate(data_tl_tr)
	# data_tl_tr = interpolate.interpolate(data_tl_tr, data_tl_tr[0][0])

	data_tl_tr = (data_tl_tr + [[0] * 3 for _ in range(600)])[0 : 600]
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
