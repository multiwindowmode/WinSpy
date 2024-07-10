import subprocess
import datetime
import pytz
import sys

# utc+8
# return class: datetime
#    2024-03-19 10:22:05.552000+08:00
def get_android_time(device_id):
    cmd = f"adb -s {device_id} shell date +%s%N"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        # Strips leading and trailing whitespace from the adb command output and stores it as a string
        timestamp_str = result.stdout.strip()

        # Extracts the first part of the timestamp (seconds since the Unix epoch) and converts it to an integer
        timestamp_sec = int(timestamp_str[:-9])

        # Extracts the last 9 characters of the timestamp (nanoseconds), converts to an integer, and then divides by 1,000,000 to convert nanoseconds to milliseconds
        timestamp_nsec = int(timestamp_str[-9:]) // 1000000

        # Creates a timezone-aware datetime object representing the time in UTC.
        # This uses the seconds part to create the datetime, then sets the microseconds part to the milliseconds value calculated above.
        utc_dt = datetime.datetime.fromtimestamp(timestamp_sec, tz=datetime.timezone.utc).replace(microsecond=timestamp_nsec * 1000)

        # Defines the UTC+8 timezone using pytz for accurate timezone conversion
        tz_utc_8 = pytz.timezone('Asia/Shanghai')

        # Converts the UTC datetime object to a timezone-aware datetime object in UTC+8 timezone
        android_time = utc_dt.astimezone(tz_utc_8)

        if not str(android_time).endswith("+08:00"):
            sys.exit(0)

        return android_time
    else:
        print("fail on getting Android date")
        return None

def compare_times(android_time):
    tz_utc_8 = pytz.timezone('Asia/Shanghai')

    # Get the current time in UTC+8
    windows_time = datetime.datetime.now(tz=tz_utc_8)
    print(f"Android time (UTC+8): {android_time.strftime('%Y-%m-%d %H:%M:%S.%f')}")
    print(f"Windows time (UTC+8): {windows_time.strftime('%Y-%m-%d %H:%M:%S.%f')}")

if __name__ == "__main__x":
    # device ID
    device_id = "8KE5T19515023226"
    device_id = "AVNS023926003923"

    res = get_android_time(device_id=device_id)
    print(res, type(res), str(res))

    android_time = get_android_time(device_id)
    if android_time:
        compare_times(android_time)

def str1_to_microsecond(time_str):  # Example input: "2024-03-21 07:38:23.740000+08:00"
    dt_with_tz = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S.%f%z")
    dt_utc = dt_with_tz.astimezone(pytz.timezone('UTC'))

    # Calculate the microsecond from Unix epoch (1970-01-01 00:00:00 UTC)
    epoch = datetime.datetime(1970, 1, 1, tzinfo=pytz.timezone('UTC'))
    microseconds_since_epoch = int((dt_utc - epoch).total_seconds() * 1e6)

    return microseconds_since_epoch

def microseconds_to_str1(microseconds_since_epoch, timezone_str = 'Asia/Shanghai'):
    # Convert microseconds since the Unix epoch to a datetime object in UTC
    epoch = datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)
    dt_utc = epoch + datetime.timedelta(microseconds=microseconds_since_epoch)
    
    # Convert UTC datetime to the desired timezone
    target_tz = pytz.timezone(timezone_str)
    dt_with_tz = dt_utc.astimezone(target_tz)
    
    # Format the datetime object into the specified string format
    time_str = dt_with_tz.strftime("%Y-%m-%d %H:%M:%S.%f%z")
    return time_str

def str2_to_microsecond(time_str):  # input: "2024-03-21 07:38:23.740"
    dt = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S.%f")

    # the timezone is UTC+8, use it to localize the datetime
    tz_utc_8 = pytz.timezone('Asia/Shanghai')  # Or any other city in UTC+8
    dt_with_tz = tz_utc_8.localize(dt)

    # Convert to UTC
    dt_utc = dt_with_tz.astimezone(pytz.timezone('UTC'))

    # Calculate microseconds since Unix epoch
    epoch = datetime.datetime(1970, 1, 1, tzinfo=pytz.timezone('UTC'))
    microseconds_since_epoch = int((dt_utc - epoch).total_seconds() * 1e6)

    return microseconds_since_epoch


def microseconds_to_str2(microseconds_since_epoch, timezone_str='Asia/Shanghai'):
    # Convert microseconds since the Unix epoch to a datetime object in UTC
    epoch = datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)
    dt_utc = epoch + datetime.timedelta(microseconds=microseconds_since_epoch)
    
    # Convert UTC datetime to the desired timezone
    target_tz = pytz.timezone(timezone_str)
    dt_with_tz = dt_utc.astimezone(target_tz)
    
    # Format the datetime object into the specified string format without timezone information
    time_str = dt_with_tz.strftime("%Y-%m-%d %H:%M:%S.%f")
    return time_str


# Test the functions
if __name__ == "__main__":
    print(str1_to_microsecond("2024-03-21 07:38:23.740000+08:00"))
    print(str2_to_microsecond("2024-03-21 07:48:23.740"))

    r = str1_to_microsecond("2024-03-21 07:38:23.740000+08:00")
    timezone_str = 'Asia/Shanghai'  # Target timezone for the conversion
    formatted_time = microseconds_to_str1(r, timezone_str)

    print(formatted_time)

    original_time_str = "2024-08-21 07:38:23.740500"
    microseconds = str1_to_microsecond(original_time_str + "+08:00")
    converted_time_str = microseconds_to_str2(microseconds)

    print("Original Time String:", original_time_str)
    print("Microseconds since epoch:", microseconds)
    print("Converted Time String:", converted_time_str)

    # Ensuring round-trip conversion consistency
    assert original_time_str == converted_time_str, "Round-trip conversion failed"
