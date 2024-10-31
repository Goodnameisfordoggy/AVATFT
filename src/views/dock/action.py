'''
Author: HDJ
StartDate: please fill in
LastEditTime: 2024-10-31 22:13:07
FilePath: \pythond:\LocalUsers\Goodnameisfordoggy-Gitee\AVATFT\src\views\dock\action.py
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
    QApplication, QWidget, QDockWidget, QVBoxLayout, QHBoxLayout,QLineEdit, QTreeWidget, QMenu, 
    QCheckBox
    )
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import Qt, Signal, QPoint

from src.ui import Ui_ActionDock
from src.modules.file import open_file
from src.modules.filter import filter_item
from src.treeWidgetItem import TreeWidgetItem
from src.modules.logger import LOG
from src import ACTION_KEYWORDS_DIR, ICON_DIR


class ActionDock(QDockWidget):
    
    # 自定义信号
    closeSignal = Signal(str)
    itemDoubleClickedSignal = Signal(str)  # 信号携带一个字符串参数
    
    def __init__(self, title='', parent=None):
        super().__init__(title, parent)
        self.setWindowTitle(self.tr("行为关键字", "window_title"))
        self.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetClosable)
        self.resize(400, 300)
        self.setObjectName('NEUTRAL')
        self.ui = Ui_ActionDock()
        self.ui.setupUi(self)
        self.__init_childItem(ACTION_KEYWORDS_DIR, self.ui.tree)
        self.__init_connections()

        self.ui.check_box.setIcon(QIcon(os.path.join(ICON_DIR, 'arrow-collapse-vertical.svg')))

            
    def __init_connections(self):
        self.ui.check_box.stateChanged.connect(self.__on_expand_checkbox_changed)
        self.ui.search_box.textChanged.connect(self.__search_tree_items)
        self.ui.tree.itemDoubleClicked.connect(self.__on_item_double_clicked)
        self.ui.tree.customContextMenuRequested.connect(self.__show_context_menu)


    def __init_childItem(self, root_dir, parent):
        # 获取目录中的所有条目，并按照原始顺序列出
        with os.scandir(root_dir) as it:
            for entry in it:
                # 如果是目录
                if entry.is_dir():
                    newItem = TreeWidgetItem(parent, [entry.name], ('package', entry.path))
                    # 递归调用，传入新的父项 newItem
                    self.__init_childItem(entry.path, newItem)
                # 如果是文件
                else:
                    newItem = TreeWidgetItem(parent, [os.path.splitext(entry.name)[0]], ('action', entry.path))
    
    def __search_tree_items(self):
        """ 搜索树控件子项，搜索框绑定操作"""
        search_text = self.ui.search_box.text().lower() # 获取搜索框的文本，并转换为小写
        root = self.ui.tree.invisibleRootItem() # 获取根项
        filter_item(root, search_text)
    
    def __on_expand_checkbox_changed(self, state: int):
        """ 复选框状态变更绑定事件 """
        if state == 2:  # 复选框选中
            self.ui.tree.expandAll()  # 展开所有项
            self.ui.check_box.setIcon(QIcon(os.path.join(ICON_DIR, 'arrow-expand-vertical.svg')))
        else:
            self.ui.tree.collapseAll()  # 收起所有项
            self.ui.check_box.setIcon(QIcon(os.path.join(ICON_DIR, 'arrow-collapse-vertical.svg')))

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
        item = self.ui.tree.itemAt(pos)
        if item:
            # 创建上下文菜单
            context_menu = QMenu(self.ui.tree)

            # 创建菜单项
            action_edit = QAction(QIcon(os.path.join(ICON_DIR, 'folder-eye.svg')), self.tr("打开文件(目录)", "menu_action_open_file_or_directory"), self)

            # 连接菜单项的触发信号
            action_edit.triggered.connect(lambda: open_file(item.path))

            # 将菜单项添加到上下文菜单
            context_menu.addAction(action_edit)

            # 显示上下文菜单
            context_menu.exec(self.ui.tree.viewport().mapToGlobal(pos))
    
    @typing.override
    def closeEvent(self, event) -> None:
        self.closeSignal.emit('close')
        return super().closeEvent(event)
    