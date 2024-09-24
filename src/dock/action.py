'''
Author: HDJ
StartDate: please fill in
LastEditTime: 2024-09-23 22:15:02
FilePath: \pythond:\LocalUsers\Goodnameisfordoggy-Gitee\VATFT\src\dock\action.py
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
import typing
import subprocess
from PySide6.QtWidgets import (
    QApplication, QWidget, QTextEdit, QLabel, QMainWindow, QDockWidget, QVBoxLayout, QLineEdit,
    QTreeWidget, QMenu
    )
from PySide6.QtGui import QScreen, QAction
from PySide6.QtCore import Qt, Signal, QPoint

from utils.file import open_file
from utils.filter import filter_item
from utils import logger
from src.treeWidgetItem import TreeWidgetItem
from src import ACTION_KEYWORDS_DIR
LOG = logger.get_logger()


class ActionDock(QDockWidget):
    
    # 自定义信号
    closeSignal = Signal(str)
    itemDoubleClickedSignal = Signal(str)  # 信号携带一个字符串参数
    
    def __init__(self, title='', parent=None):
        super().__init__(title, parent)
        self.setWindowTitle('行为关键字')
        self.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetClosable)
        self.resize(400, 300)
        self.__initUI()
        
    def __initUI(self):
        self.center_widget = QWidget(self)
        self.setWidget(self.center_widget)
        center_widget_layout = QVBoxLayout(self.center_widget)
        
        # 搜索框
        self.search_box = QLineEdit(self)
        center_widget_layout.addWidget(self.search_box)
        self.search_box.setPlaceholderText("请输入搜索项，按Enter搜索")
        self.search_box.textChanged.connect(self.__search_tree_items)
        

        # 树控件
        self.tree = QTreeWidget()
        center_widget_layout.addWidget(self.tree)
        self.tree.setHeaderHidden(True) # 隐藏表头
        # 拖拽功能
        self.tree.setDragEnabled(True) # 能否拖拽
        self.tree.setAcceptDrops(False) # 能否放置
        self.tree.setDropIndicatorShown(True) # 是否启用放置指示器
        self.tree.setDefaultDropAction(Qt.CopyAction) # 放置操作 (MoveAction, CopyAction, LinkAction: 创建一个链接或引用)
        self.tree.itemDoubleClicked.connect(self.__on_item_double_clicked)
        # 连接右键菜单事件
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.__show_context_menu)
        # 子项
        self.__initChildItem(ACTION_KEYWORDS_DIR, self.tree)
    

    def __initChildItem(self, root_dir, parent):
        # 获取目录中的所有条目，并按照原始顺序列出
        with os.scandir(root_dir) as it:
            for entry in it:
                # 如果是目录
                if entry.is_dir():
                    newItem = TreeWidgetItem(parent, [entry.name], ('package', entry.path))
                    # 递归调用，传入新的父项 newItem
                    self.__initChildItem(entry.path, newItem)
                # 如果是文件
                else:
                    newItem = TreeWidgetItem(parent, [os.path.splitext(entry.name)[0]], ('action', entry.path))
    
    def __search_tree_items(self):
        """ 搜索树控件子项，搜索框绑定操作"""
        search_text = self.search_box.text().lower() # 获取搜索框的文本，并转换为小写
        root = self.tree.invisibleRootItem() # 获取根项
        filter_item(root, search_text)
    
    def __on_item_double_clicked(self, item: TreeWidgetItem, column):
        """ 树控件子项双击事件 """
        try:
            if item.type == 'action':
                self.itemDoubleClickedSignal.emit(item.path) # 发送信号
        except AttributeError:
            pass
    
    def __show_context_menu(self, pos: QPoint):
        """ 树控件子项右键菜单事件 """
        # 获取点击的项
        item = self.tree.itemAt(pos)
        if item:
            # 创建上下文菜单
            context_menu = QMenu(self)

            # 创建菜单项
            action_edit = QAction("打开文件(目录)", self)

            # 连接菜单项的触发信号
            action_edit.triggered.connect(lambda: open_file(item.path))

            # 将菜单项添加到上下文菜单
            context_menu.addAction(action_edit)

            # 显示上下文菜单
            context_menu.exec(self.tree.viewport().mapToGlobal(pos))
    
    @typing.override
    def closeEvent(self, event) -> None:
        self.closeSignal.emit('close')
        return super().closeEvent(event)
    

if __name__ == '__main__':
    app = QApplication([])
    window = ActionDock()
    window.show()
    app.exec()