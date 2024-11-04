'''
Author: HDJ
StartDate: please fill in
LastEditTime: 2024-11-04 09:33:31
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
    QWidget, QDockWidget, QVBoxLayout, QHBoxLayout,QLineEdit, QTreeWidget, QCheckBox
    )
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, Signal

from src import ICON_DIR
from src.modules.logger import get_global_logger
LOG = get_global_logger()

class ActionDock(QDockWidget):
    
    # 自定义信号
    closeSignal = Signal(str)
    itemDoubleClickedSignal = Signal(str)
    updateChildrenItemSignal = Signal()
    
    def __init__(self, title='', parent=None):
        super().__init__(title, parent)
        self.setWindowTitle(self.tr("行为关键字", "window_title"))
        self.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetClosable)
        self.resize(400, 300)
        self.setObjectName('NEUTRAL')
        self.setupUi()

    def setupUi(self):
        self.center_widget = QWidget(self)
        self.setWidget(self.center_widget)
        self.center_widget_layout = QVBoxLayout(self.center_widget)
        
        self.layout = QHBoxLayout()
        self.center_widget_layout.addLayout(self.layout)
        # 复选框
        self.check_box = QCheckBox(self)
        self.check_box.setIcon(QIcon(os.path.join(ICON_DIR, 'arrow-collapse-vertical.svg')))
        
        self.check_box.setObjectName('NEUTRAL')
        self.layout.addWidget(self.check_box, 1)
        # 搜索框
        self.search_box = QLineEdit(self)
        self.search_box.setObjectName('NEUTRAL')
        self.search_box.setPlaceholderText(self.tr("请输入搜索项，按Enter搜索", "search_box_placeholder_text"))
        self.layout.addWidget(self.search_box, 99)
        
        # 树控件
        self.tree = QTreeWidget(self)
        self.tree.setObjectName('NEUTRAL') 
        self.center_widget_layout.addWidget(self.tree)
        self.tree.setHeaderHidden(True) # 隐藏表头
        # 拖拽功能
        self.tree.setDragEnabled(True) # 能否拖拽
        self.tree.setAcceptDrops(False) # 能否放置
        self.tree.setDropIndicatorShown(True) # 是否启用放置指示器
        self.tree.setDefaultDropAction(Qt.CopyAction) # 放置操作 (MoveAction, CopyAction, LinkAction: 创建一个链接或引用)
        # 设置右键菜单
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
    
    @typing.override
    def closeEvent(self, event) -> None:
        self.closeSignal.emit('close')
        return super().closeEvent(event)
    