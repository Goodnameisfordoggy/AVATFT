from PySide6.QtWidgets import QTreeWidgetItem


def filter_item(item: QTreeWidgetItem, search_text: str):
    """ 
    筛选符合条件的子项，遍历子项，递归搜索
    
    :param item: 根节点（项）
    """
    # 当前项处理
    item_text = item.text(0).lower()  # 获取项的文本，并转换为小写
    match = search_text in item_text  # 检查项的文本是否包含搜索内容

    # 对所有子项进行同样的处理
    for j in range(item.childCount()):
        child_item = item.child(j)
        match = filter_item(child_item, search_text) or match # 如果任何一个子项匹配，那么其父项也应当被视为匹配

    # 根据是否匹配来设置当前项是否可见
    item.setHidden(not match)
    return match

def input_type_identify(input_value: str):
    """
    识别输入内容的类型， 并返回对应的值。
    
    :param input_value: 输入内容一般为字符串类型
    """
    # 1. 先判断是否为 None（空字符串或 None 都视为 None）
    if input_value is None or input_value.strip() == "":
        return None

    # 2. 再判断是否为 bool 类型 ('True'/'False' 不区分大小写)
    lower_value = input_value.strip().lower()
    if lower_value == "true":
        return True
    elif lower_value == "false":
        return False

    # 3. 判断是否为 int 类型
    try:
        int_value = int(input_value)
        # 排除 float 的特殊情况（带小数点但整数部分为 0）
        if "." not in input_value:
            return int_value
    except ValueError:
        pass

    # 4. 判断是否为 float 类型
    try:
        float_value = float(input_value)
        return float_value
    except ValueError:
        pass

    # 5. 如果没有匹配上其他类型，则默认返回 str
    return input_value