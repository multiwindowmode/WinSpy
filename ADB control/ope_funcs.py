import subprocess
import sys

def exit_0(result):
    if result.returncode:
        print(result.stderr)
        sys.exit(result.returncode)

def runcommand(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    exit_0(result)

def force_stop_app(device_id, package_name):
    command = f"adb -s {device_id} shell am force-stop {package_name}"
    runcommand(command)

def kill_app(device_id, package_name):
    command = f"adb -s {device_id} shell am kill {package_name}"
    runcommand(command)

def kill_background(device_id):
    command = f"adb -s {device_id} shell am kill-all"
    runcommand(command)

# def open_url_with_default_browser(device_id, url):
#     command = f"adb -s {device_id} shell am start -a android.intent.action.VIEW -d {url}"
#     result = subprocess.run(command, shell=True, capture_output=True, text=True)
#     exit_0(result)

def open_url_with_browser(device_id, url, package_name):
    command = f"adb -s {device_id} shell am start -a android.intent.action.VIEW -d {url} {package_name}"
    runcommand(command)

# def open_black_page(device_id, package_name):
#     command = f"adb -s {device_id} shell am start --windowingMode=auto -a android.intent.action.VIEW -d https://www.example.com {package_name}"
#     result = subprocess.run(command, shell=True, capture_output=True, text=True)
#     exit_0(result)

def tap_xy(device_id, x, y):
    command = f"adb -s {device_id} shell input tap {x} {y}"
    runcommand(command)

def send_swipe(device_id, pa, pb, dur):
    command = f"adb -s {device_id} shell input swipe {pa[0]} {pa[1]} {pb[0]} {pb[1]} {dur}"
    runcommand(command)

def send_delete(device_id, num):
    command = f"adb -s {device_id} shell input"
    for _ in range(num):
        command = command + " keyevent 67"

    runcommand(command)

def send_enter(device_id):
    command = f"adb -s {device_id} shell input keyevent 66"
    runcommand(command)

def send_string(device_id, ss):
    command = f"adb -s {device_id} shell input text {ss}"
    runcommand(command)

def send_home(device_id):
    command = f"adb -s {device_id} shell input keyevent KEYCODE_HOME"
    runcommand(command)

def send_prevent_screen_off(device_id):
    command = f"adb -s {device_id} shell settings put system screen_off_timeout 2147483647"
    runcommand(command)

def check_screen_on(device_id):
    cmd = f"adb -s {device_id} shell dumpsys power"
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    result = str(result)
    msg_true = 'mHoldingDisplaySuspendBlocker=true'
    msg_false = 'mHoldingDisplaySuspendBlocker=false'
    assert msg_true in result or msg_false in result
    return msg_true in result

def check_battery_level(device_id):
    cmd = f"adb -s {device_id} shell dumpsys battery"
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output = result.stdout
    level = None
    for line in output.splitlines():
        if 'level' in line:
            level = int(line.split(':')[1].strip())
            break
    assert level
    return level >= 50

def log(s1, path):
    with open(path, "a") as f:
        f.write(s1 + "\n")

if __name__ == "__main__":
    did = "AVNS023926003923"
    print(check_battery_level(did))