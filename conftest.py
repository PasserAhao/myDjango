import os

# 告诉pytest django的settings配置路径, 不然pytest找不到setting会报错
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")


def pytest_runtest_call(item):
    print(f"\n{item.name} logs:")


def pytest_runtest_teardown(item, nextitem):
    print(f"\n{item.name} logs end ~~~ \n")
