from PySide6.QtWidgets import QTreeWidgetItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

class TreeWidgetItem(QTreeWidgetItem):
    """
    Data(tuple):
        0----type
        1----path
        2----draggable
        3----AcceptDrops
    """
    def __init__(self, parent, text: list, data: tuple = (), icon_path: str = '', editable: bool = False):
        super().__init__(parent, text)
        self.__data = data
        # 添加数据
        if self.__data:
            for i in range(len(self.__data)):
                if self.__data[i]:
                    self.setData(i, Qt.UserRole, self.__data[i])
        # 添加图标
        icon = QIcon(icon_path)
        self.setIcon(0, icon)  # 在第一列添加图标
        
        # 只设置整个 item 可编辑，这会影响到所有列
        if editable:
            self.setFlags(self.flags() | Qt.ItemIsEditable)

