import os
from dotenv import load_dotenv
RUN_MODEL = os.environ.get("RUN_MODEL", "local")
DJANGO_CONF_MODULE = "config.{}".format(RUN_MODEL)

if RUN_MODEL == "local":
    load_dotenv("envs/local.env")

try:
    _module = __import__(DJANGO_CONF_MODULE, globals(), locals(), ["*"])
except ImportError as e:
    raise ImportError("Could not import config '{}' (Is it on sys.path?): {}".format(DJANGO_CONF_MODULE, e))

for _setting in dir(_module):
    if _setting == _setting.upper():
        locals()[_setting] = getattr(_module, _setting)
