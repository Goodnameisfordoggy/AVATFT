'''
Author: HDJ
StartDate: please fill in
LastEditTime: 2024-08-29 21:46:41
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
import sys
import subprocess
from PySide6.QtWidgets import (
    QApplication, QWidget, QTextEdit, QLabel, QMainWindow, QDockWidget, QVBoxLayout, QLineEdit,
    QTreeWidget, QTreeWidgetItem, QMenu
    )
from PySide6.QtGui import QScreen, QAction
from PySide6.QtCore import Qt, Signal, QPoint

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
        # 连接右键菜单事件
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.show_context_menu)
        # 子项
        first_iteration = True
        for root, dirs, files in os.walk(ACTION_KEYWORDS_PATH):
            if first_iteration:
                first_iteration = False
                continue
            rootItem = QTreeWidgetItem(self.tree, [os.path.basename(root)])
            rootItem.setData(0, Qt.UserRole, {'type': 'package', 'path': root, })
            for file_name in files:
                childItem = QTreeWidgetItem(rootItem, [os.path.splitext(file_name)[0]])
                childItem.setData(0, Qt.UserRole, {'type': 'action', 'path': os.path.join(root, file_name), })
            
    def on_item_double_clicked(self, item, column):
        """ 树控件子项双击事件 """
        try:
            if item.data(0, Qt.UserRole).get('type') == 'action':
                self.item_double_clicked_signal.emit(item.data(0, Qt.UserRole).get('path')) # 发送信号
        except AttributeError:
            pass
    
    def show_context_menu(self, pos: QPoint):
        """ 树控件子项右键菜单事件 """
        # 获取点击的项
        item = self.tree.itemAt(pos)
        if item:
            # 创建上下文菜单
            context_menu = QMenu(self)

            # 创建菜单项
            action_edit = QAction("打开文件(目录)", self)

            # 连接菜单项的触发信号
            action_edit.triggered.connect(lambda: self.open_file(item.data(0, Qt.UserRole).get('path')))

            # 将菜单项添加到上下文菜单
            context_menu.addAction(action_edit)

            # 显示上下文菜单
            context_menu.exec(self.tree.viewport().mapToGlobal(pos))
    
    def open_file(self, path: str):
        """ 调用系统默认程序打开文件 """
        if sys.platform == "win32":
            subprocess.Popen(["start", path], shell=True)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", path])
        else:  # Linux
            subprocess.Popen(["xdg-open", path])


if __name__ == '__main__':
    app = QApplication([])
    window = ActionDock()
    window.show()
    app.exec()