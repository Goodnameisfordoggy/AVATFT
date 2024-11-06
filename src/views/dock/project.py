'''
Author: HDJ
StartDate: please fill in
LastEditTime: 2024-11-04 23:44:02
FilePath: \pythond:\LocalUsers\Goodnameisfordoggy-Gitee\AVATFT\src\views\dock\project.py
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
import typing
from PySide6.QtWidgets import (
    QWidget, QDockWidget, QVBoxLayout, QLineEdit, QTreeWidget, QTreeWidgetItem, QMenu, QFileDialog
	)
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import Qt, Signal

from src.modules.logger import get_global_logger
LOG = get_global_logger()

class ProjectDock(QDockWidget):
    
    # 自定义信号
    closeSignal = Signal(str)
    distorySignal = Signal()
    getCheckedModulesSignal = Signal(str)
    itemDoubleClickedSignal = Signal(str)
    loadProjectSignal = Signal(str)
    loadHistoryProjectSiganl = Signal()
    newProjectSignal = Signal(str)
    operateResponseSignal = Signal(list)
    
    
    def __init__(self, title='', parent=None):
        super().__init__(title, parent)
        self.setWindowTitle(self.tr("项目", "window_title"))
        self.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetClosable)
        self.setObjectName('NEUTRAL')
        self.setupUi()

    def setupUi(self):
        self.center_widget = QWidget(self)
        self.setWidget(self.center_widget)
        self.center_widget_layout = QVBoxLayout(self.center_widget)
        
        # 搜索框
        self.search_box = QLineEdit(self)
        self.search_box.setObjectName('NEUTRAL')
        self.search_box.setPlaceholderText(self.tr("请输入搜索项，按Enter搜索", "search_box_placeholder_text"))
        self.center_widget_layout.addWidget(self.search_box)

        # 树控件
        self.tree = QTreeWidget(self)
        self.tree.setObjectName('NEUTRAL') 
        self.tree.setHeaderHidden(True) # 隐藏表头
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu) # 使用自定义菜单
        self.center_widget_layout.addWidget(self.tree)
    
    @typing.override
    def closeEvent(self, event) -> None:
        self.closeSignal.emit('close')
        return super().closeEvent(event)