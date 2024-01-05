def get_settings_from_module(module, is_upper=True):
    setting_items = {}
    for _setting in dir(module):
        if is_upper and not _setting.isupper():
            continue
        setting_items[_setting] = getattr(module, _setting)
    return setting_items
