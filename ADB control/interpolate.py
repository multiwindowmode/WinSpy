import android_time
from collections import deque

microsecond_per_second = 1000000
millisecond_per_second = 1000

def interpolate(dq1: deque[tuple[int, int, int, int]], begin_time: int):
    dq2 = [list(i) for i in dq1] # convert deque[tuple[...]] to list[list[...]]
    dq = [] 

    # merge time confict: t[i-1] == t[i]
    for idx, tuple4 in enumerate(dq2):
        if idx == 0 or tuple4[0] != dq2[idx - 1][0]:
            dq.append(tuple4)
        else:
            for i in range(1, 4):
                dq[-1][i] += tuple4[i]

    def time_idx(t): # index: dt // 1000
        return (t - begin_time) // millisecond_per_second

    # for each time interval (1ms)
    time_point_val = []

    # time_point_val[i][j] += val
    def update(i, j, val): 
        while len(time_point_val) <= i or len(time_point_val) % 10:
            time_point_val.append([0.0 for _ in range(3)])
        time_point_val[i][j] += val

    for idx, (tm, *num) in enumerate(dq):
        if idx:
            pre_tm = dq[idx - 1][0]
            time_len = (tm - pre_tm) / millisecond_per_second # mill sec

            while True: # from tm to pre_tm, (pre_tm, tm]
                for i in range(3):
                    update(time_idx(tm), i, num[i] / time_len)
                tm -= millisecond_per_second
                if tm <= pre_tm:
                    break
    
    assert len(time_point_val) % 10 == 0

    time_point_val10 = []
    for i in range(0, len(time_point_val), 10): # sum(i : i+10)
        z = [0.0 for _ in range(3)]
        for j in range(i, i + 10):
            for k in range(3):
                z[k] += time_point_val[j][k]
        time_point_val10.append(z)

    return [[int(j) for j in i] for i in time_point_val10]

if __name__ == "__main__": # test
    deque_android = deque()
    with open("interpolate_test.txt", 'r') as f:
        for i in f.readlines():
            try:
                a, b, n0, n1, n2 = i.split()
            except:
                break
            assert len(a) == len("2024-03-20") and len(b) == len("17:15:58.832")
            micro_time = android_time.str2_to_microsecond(a + " " + b)
            deque_android.append((micro_time, int(n0), int(n1), int(n2)))

    re = interpolate(deque_android, deque_android[0][0])
    for i in re:
        print("ss", i)

def no_interpolate(dq1: deque[tuple[int, int, int, int]]):
    return [[*num] for _, *num in dq1]