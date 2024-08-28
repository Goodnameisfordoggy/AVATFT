'''
Author: HDJ
StartDate: please fill in
LastEditTime: 2024-08-29 00:23:29
FilePath: \pythond:\LocalUsers\Goodnameisfordoggy-Gitee\VATFT\dockWidget_action.py
Description: 

				*		写字楼里写字间，写字间里程序员；
				*		程序人员写程序，又拿程序换酒钱。
				*		酒醒只在网上坐，酒醉还来网下眠；
				*		酒醉酒醒日复日，网上网下年复年。
				*		但愿老死电脑间，不愿鞠躬老板前；
				*		奔驰宝马贵者趣，公交自行程序员。
				*		别人笑我忒疯癫，我笑自己命太贱；
				*		不见满街漂亮妹，哪个归得程序员？    
Copyright (c) 2024 by HDJ, All Rights Reserved. 
'''
import os
from PySide6.QtWidgets import (
    QApplication, QWidget, QTextEdit, QLabel, QMainWindow, QDockWidget, QVBoxLayout, QLineEdit,
    QTreeWidget, QTreeWidgetItem
    )
from PySide6.QtGui import QScreen
from PySide6.QtCore import Qt, Signal

ACTION_KEYWORDS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'action_keywords')

class ActionDock(QDockWidget):
    
    # 自定义信号
    item_double_clicked_signal = Signal(str)  # 信号携带一个字符串参数

    def __init_subclass__(cls) -> None:
        return super().__init_subclass__()
    
    def __init__(self, title='', parent=None):
        super().__init__(title, parent)
        self.setWindowTitle('行为关键字')
        self.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetClosable)
        self.resize(400, 300)
        self.initUI()
        
    
    def initUI(self):
        self.center_widget = QWidget(self)
        self.setWidget(self.center_widget)
        center_widget_layout = QVBoxLayout(self.center_widget)
        
        # 搜索框
        self.search_box = QLineEdit(self)
        center_widget_layout.addWidget(self.search_box)
        self.search_box.setPlaceholderText("请输入搜索项，按Enter搜索")
        # self.search_box.textChanged.connect()
        

        # 树控件
        self.tree = QTreeWidget()
        center_widget_layout.addWidget(self.tree)
        self.tree.setHeaderHidden(True) # 隐藏表头
        # 拖拽功能
        self.tree.setDragEnabled(True) # 能否拖拽
        self.tree.setAcceptDrops(False) # 能否放置
        self.tree.setDropIndicatorShown(True) # 是否启用放置指示器
        self.tree.setDefaultDropAction(Qt.LinkAction) # 放置操作 (MoveAction, CopyAction, LinkAction: 创建一个链接或引用)
        self.tree.itemDoubleClicked.connect(self.on_item_double_clicked)
        # 子项
        first_iteration = True
        for root, dirs, files in os.walk(ACTION_KEYWORDS_PATH):
            if first_iteration:
                first_iteration = False
                continue
            rootItem = QTreeWidgetItem(self.tree, [os.path.basename(root)])
            for file_name in files:
                childItem = QTreeWidgetItem(rootItem, [os.path.splitext(file_name)[0]])
                childItem.setData(0, Qt.UserRole, {'type': 'action', 'action_path': os.path.join(root, file_name), })
            
    def on_item_double_clicked(self, item, column):
        """ 树控件子项双击事件 """
        try:
            if item.data(0, Qt.UserRole).get('type') == 'action':
                # print(f"Item '{item.text(0)}' in column {column} was double-clicked.")
                self.item_double_clicked_signal.emit(item.data(0, Qt.UserRole).get('action_path'))
        except AttributeError:
            pass
    
if __name__ == '__main__':
    app = QApplication([])
    window = ActionDock()
    window.show()
    app.exec()