import bisect
import csv

# 0.5ms
def read_then_norm(ftap):
    res = list()
    with open(ftap, 'r') as f:
        for idx, i in enumerate(f.readlines()):
            j = i.split()

            temp = []
            for k in [6, 9, 12]:
                s = j[k]
                if s.endswith(','):
                    s = s[:-1]
                temp.append(int(s))
            
            res.append(temp) # [timestamp, x, y]
    return res

def read_then_norm2(fimu):
    res0 = list()
    res1 = list()
    with open(fimu, 'r') as f:

        for idx, i in enumerate(f.readlines()):
            j = i.split()
            temp = []

            for k in range(7, 16 + 1, 3): # 7, 10, 13, 16
                try:
                    s = j[k]
                except:
                    print(j, idx)

                if s.endswith(','):
                    s = s[:-1]
                if '.' in s:
                    temp.append(float(s))
                else:
                    temp.append(int(s))
            
            if i[0] == 'A':
                res0.append(temp)
            else:
                res1.append(temp)

    return res0, res1


def get_pair(arr, timestamp): # [x - 0.5s, x + 0.5s]
    nano_per_sec = 1000000000

    tl = timestamp - nano_per_sec // 2
    tr = timestamp + nano_per_sec // 2
    res = [[0.0, 0.0, 0.0] for _ in range(2000)]
    pos_l = bisect.bisect_left(arr, tl, key = lambda x : x[0])

    for i in range(pos_l, int(1e100)):
        at = (arr[i][0] - tl) // (nano_per_sec // 2000)
        if at >= 2000:
            break
        for j in range(3):
            res[at][j] += arr[i][j + 1]
    return res

# ff =  "collected_data/expand_2h_regression"
# ff =  "collected_data/expand_class10_ui1"
# ff =  "collected_data/expand_class10_ui2_phone"

ff =  "collected_data/mix_P30_2h_regression"
# ff =  "collected_data/mix_P30_2h_class10_ui1"
# ff =  "collected_data/mix_P30_2h_class10_ui2"

# ff =  "collected_data/not_expand_desktop"
# ff =  "collected_data/not_expand_desktop2"
# ff =  "collected_data/not_expand_desktop3_2hour"
# ff =  "collected_data/not_expand_hand"
# ff =  "collected_data/not_expand_90min_12classes"
# ff =  "collected_data/not_expand_90min_12_classes_phone"

ftap = f"./{ff}/tap.txt"
fimu = f"./{ff}/imu.txt"
fcsv = f"./{ff}/data.csv"

list_tap = read_then_norm(ftap)
list_imu0, list_imu1 = read_then_norm2(fimu)

qs = []
for timestamp, x, y in list_tap:

    g = get_pair(list_imu0, timestamp) # 2000 * 3
    h = get_pair(list_imu1, timestamp) # 2000 * 3

    q = []
    for u in [g, h]:
        for i in range(3):
            assert len(g) == 2000
            for j in range(2000):
                q.append(u[j][i])

    assert len(q) == 2000 * 6

    q.append(x)
    q.append(y)
    qs.append(q)

with open(fcsv, mode='w', newline='') as file:
    writer = csv.writer(file)
    for i in qs:
        writer.writerow(i)