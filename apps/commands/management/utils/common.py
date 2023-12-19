

def dynamic_importer(path: str):
    """
    根据函数路径动态导入并返回该函数。
    :param path: 表示要调用的函数的完整路径的字符串。
    :return: 调用函数的输出。
    """
    try:
        sep_index = path.rfind(".")
        if sep_index < 0:
            raise InvalidPath()
        module_path = path[:sep_index]
        class_or_func_name = path[sep_index + 1:]
        module = import_module(module_path)
        return getattr(module, class_or_func_name)
    except (ValueError, AttributeError, ImportError) as e:
        raise InvalidPath()



