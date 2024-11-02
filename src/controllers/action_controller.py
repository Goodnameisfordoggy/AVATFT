'''
Author: HDJ
StartDate: please fill in
LastEditTime: 2024-11-03 00:42:12
FilePath: \pythond:\LocalUsers\Goodnameisfordoggy-Gitee\AVATFT\src\controllers\action_controller.py
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
import json
import yaml
import typing
import shutil
from PySide6.QtWidgets import (
    QWidget, QDockWidget, QVBoxLayout, QLineEdit, QTreeWidget, QTreeWidgetItem, QMenu, QFileDialog
	)
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import QObject, Qt, QPoint, Signal, Slot

from src.modules import open_file, load_file_content, save_file_content, filter_item
from src.treeWidgetItem import TreeWidgetItem
from src.views import NameInputDialogBox, ReconfirmDialogBox
from src import PROJECTS_DIR, CONFIG_DIR, ICON_DIR, ACTION_KEYWORDS_DIR
from src.modules.logger import get_global_logger
LOG = get_global_logger()

class ActionController(QObject):
    
    def __init__(self, action_dock):
        from src.views import ActionDock
        self.view: ActionDock = action_dock
        self.__init_connections()
        self.__connect_custom_signals()

    def __init_connections(self):
        """连接内置事件信号与槽函数"""
        self.view.check_box.stateChanged.connect(self.__on_expand_checkbox_changed)
        self.view.search_box.textChanged.connect(self.__search_tree_items)
        self.view.tree.itemDoubleClicked.connect(self.__on_item_double_clicked)
        self.view.tree.customContextMenuRequested.connect(self.__show_context_menu)
    
    def __connect_custom_signals(self):
        """连接自定义信号与槽函数"""
        self.view.updateChildrenItemSignal.connect(lambda :self.__init_childItem(ACTION_KEYWORDS_DIR, self.view.tree))

    @Slot(int)
    def __on_expand_checkbox_changed(self, state: int):
        """ 复选框状态变更绑定事件 """
        if state == 2:  # 复选框选中
            self.view.tree.expandAll()  # 展开所有项
            self.view.check_box.setIcon(QIcon(os.path.join(ICON_DIR, 'arrow-expand-vertical.svg')))
        else:
            self.view.tree.collapseAll()  # 收起所有项
            self.view.check_box.setIcon(QIcon(os.path.join(ICON_DIR, 'arrow-collapse-vertical.svg')))
    
    @Slot()
    def __search_tree_items(self):
        """ 搜索树控件子项，搜索框绑定操作"""
        search_text = self.view.search_box.text().lower() # 获取搜索框的文本，并转换为小写
        root = self.view.tree.invisibleRootItem() # 获取根项
        filter_item(root, search_text)

    @Slot(TreeWidgetItem, int)
    def __on_item_double_clicked(self, item: TreeWidgetItem, column):
        """ 树控件子项双击事件 """
        try:
            if item.type == 'action':
                self.view.itemDoubleClickedSignal.emit(item.path) # 发送信号
        except AttributeError:
            pass
    
    @Slot(QPoint)
    def __show_context_menu(self, pos: QPoint):
        """ 树控件子项右键菜单事件 """
        # 获取点击的项
        item = self.view.tree.itemAt(pos)
        if item:
            # 创建上下文菜单
            context_menu = QMenu(self.view.tree)

            # 创建菜单项
            action_edit = QAction(QIcon(os.path.join(ICON_DIR, 'folder-eye.svg')), self.tr("打开文件(目录)", "menu_action_open_file_or_directory"), self.view.tree)

            # 连接菜单项的触发信号
            action_edit.triggered.connect(lambda: open_file(item.path))

            # 将菜单项添加到上下文菜单
            context_menu.addAction(action_edit)

            # 显示上下文菜单
            context_menu.exec(self.view.tree.viewport().mapToGlobal(pos))
    
    @Slot(str, QTreeWidget)
    def __init_childItem(self, root_dir: str, parent: QTreeWidget | TreeWidgetItem):
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