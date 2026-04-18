try:
    import urequests as _requests
except ImportError:
    _requests = None


def post_reading(url, payload):
    if _requests is None:
        print("[upload] urequests unavailable")
        return False
    try:
        resp = _requests.post(url, json=payload)
        ok = 200 <= resp.status_code < 300
        resp.close()
        if ok:
            print("[upload] ok:", resp.status_code)
        else:
            print("[upload] server error:", resp.status_code)
        return ok
    except Exception as e:
        print("[upload] error:", e)
        return False
