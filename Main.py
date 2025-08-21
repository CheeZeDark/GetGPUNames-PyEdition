import ctypes

# Load user32.dll
user32 = ctypes.windll.user32

# Define DISPLAY_DEVICEW structure
class DISPLAY_DEVICEW(ctypes.Structure):
    _fields_ = [
        ("cb", ctypes.c_uint32),
        ("DeviceName", ctypes.c_wchar * 32),
        ("DeviceString", ctypes.c_wchar * 128),
        ("StateFlags", ctypes.c_uint32),
        ("DeviceID", ctypes.c_wchar * 128),
        ("DeviceKey", ctypes.c_wchar * 128)
    ]

EnumDisplayDevices = user32.EnumDisplayDevicesW
EnumDisplayDevices.argtypes = [ctypes.c_wchar_p, ctypes.c_uint32, ctypes.POINTER(DISPLAY_DEVICEW), ctypes.c_uint32]
EnumDisplayDevices.restype = ctypes.c_bool

def get_unique_gpus():
    seen = set()
    gpus = []
    i = 0
    while True:
        device = DISPLAY_DEVICEW()
        device.cb = ctypes.sizeof(DISPLAY_DEVICEW)

        # Enumerate display adapters (lpDevice = None)
        if not EnumDisplayDevices(None, i, ctypes.byref(device), 0):
            break  # No more devices

        gpu_name = device.DeviceString.strip()
        if gpu_name and gpu_name not in seen:
            # Exclude Microsoft Basic Render Driver if you want
            if "Microsoft Basic Render Driver" not in gpu_name:
                seen.add(gpu_name)
                gpus.append(gpu_name)

        i += 1

    return gpus

# Test
gpu_list = get_unique_gpus()
if gpu_list:
    print("Detected GPUs:")
    for gpu in gpu_list:
        print("-", gpu)
else:
    print("Pls update your GPUs or Check Video Card Connector!!!")
