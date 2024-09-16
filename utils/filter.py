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