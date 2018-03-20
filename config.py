import os

BASE_DIR = os.path.dirname(__file__)

options = {
    "port": 8003,
}

settings = {
    "debug": True,
    "static_path": os.path.join(BASE_DIR, "static"),
    "template_path": os.path.join(BASE_DIR, "templates"),
    # "autoreload": True,
    # "complited_template_cache":False,
    "xsrf_cookies": True,
    "login_url": "/login"
}
