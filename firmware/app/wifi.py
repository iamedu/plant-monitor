try:
    import network
    import time as _time
except ImportError:
    network = None
    _time = None


def connect(ssid, password, timeout_s=20):
    if network is None:
        print("[wifi] network module unavailable")
        return False
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    if sta.isconnected():
        return True
    sta.connect(ssid, password)
    deadline = _time.time() + timeout_s
    while _time.time() < deadline:
        if sta.isconnected():
            print("[wifi] connected:", sta.ifconfig()[0])
            return True
        _time.sleep(0.5)
    print("[wifi] connection timed out")
    return False


def disconnect():
    if network is None:
        return
    sta = network.WLAN(network.STA_IF)
    sta.disconnect()
    sta.active(False)
