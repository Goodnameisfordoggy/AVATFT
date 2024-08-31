'''
Author: HDJ
StartDate: please fill in
LastEditTime: 2024-08-31 16:13:25
FilePath: \pythond:\LocalUsers\Goodnameisfordoggy-Gitee\VATFT\dockWidget_edit.py
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
import json
import yaml
from PySide6.QtWidgets import (
    QApplication, QLabel, QMainWindow, QDockWidget, QVBoxLayout, QWidget, QLineEdit, QTreeWidget,
    QMenu, QPushButton
    )
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, QPoint
from treeWidgetItem import TreeWidgetItem, ActionItem, ModuleItem

class EditDock(QDockWidget):
    
    def __init__(self, title='', parent=None):
        super().__init__(title, parent)
        
        # QDockWidget.NoDockWidgetFeatures        禁用所有特性，停靠窗口将不能移动、浮动或关闭。
        # QDockWidget.DockWidgetMovable           允许停靠窗口在主窗口中移动（拖动）。
        # QDockWidget.DockWidgetFloatable         允许停靠窗口浮动到主窗口之外成为独立窗口。
        # QDockWidget.DockWidgetClosable          允许用户关闭停靠窗口。
        # QDockWidget.DockWidgetVerticalTitleBar  显示垂直标题栏，这个特性仅在某些平台和样式中有效。
        # QDockWidget.DockWidgetAutoHide          允许停靠窗口自动隐藏。当用户将鼠标移到窗口边缘时，停靠窗口将会自动显示出来，移开鼠标时将会自动隐藏。
        # QDockWidget.DockWidgetFloatable         允许停靠窗口浮动，使其可以脱离主窗口作为独立的浮动窗口显示。
        # QDockWidget.DockWidgetMovable           允许停靠窗口在主窗口中进行移动。
        self.setFeatures(QDockWidget.NoDockWidgetFeatures | QDockWidget.DockWidgetClosable)
        self.setTitleBarWidget(QLabel('   测试用例编辑区'))
        self.initUI()
    
    def initUI(self):
        self.center_widget = QWidget(self)
        self.setWidget(self.center_widget)
        center_widget_layout = QVBoxLayout(self.center_widget)
        
        # 搜索框
        self.search_box = QLineEdit(self)
        self.search_box.setPlaceholderText("请输入搜索项，按Enter搜索")
        # self.search_box.textChanged.connect()
        center_widget_layout.addWidget(self.search_box)

        # 树状控件
        self.tree = TreeWidget()
        center_widget_layout.addWidget(self.tree)

        # 运行按钮
        self.operation_btn = QPushButton(self, text='开始测试')
        center_widget_layout.addWidget(self.operation_btn)

    def display_action_details(self, action_path:str):
        """ 
        展示action的详细信息 
        
        action_path: 由信号携带
        """
        # 清空树控件
        self.tree.clear()
        # 创建action子项
        actionItem = ActionItem(self.tree, data=('action', action_path)) # 配置文件(yaml)有列表结构
        # 展开子项
        actionItem.setExpanded(True)
        # 自动调整所有列的宽度
        self.tree.resizeColumnToContents(0)
        self.tree.resizeColumnToContents(1)
        self.tree.resizeColumnToContents(2)
    
    def display_module_details(self, module_path:str):
        """ 
        展示module的详细信息 
        
        module_path: 由信号携带
        """
        # 清空树控件
        self.tree.clear()
        # 创建module子项
        moduleItem = ModuleItem(self.tree, data=('module', module_path))
        # 自动调整所有列的宽度
        self.tree.resizeColumnToContents(0)
        self.tree.resizeColumnToContents(1)
        self.tree.resizeColumnToContents(2)

class TreeWidget(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.setColumnCount(3) # 列数
        self.setHeaderLabels(['参数描述', '参数名称', '参数值'])
        self.setDragEnabled(False) # 能否拖拽
        self.setAcceptDrops(True) # 能否放置
        self.setDropIndicatorShown(True) # 是否启用放置指示器
        self.setDefaultDropAction(Qt.MoveAction) # 放置操作 (MoveAction, CopyAction, LinkAction: 创建一个链接或引用)
        # 连接右键菜单事件
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        

    def edit(self, index, trigger, event):
        # 仅允许编辑第3列的文本
        if index.column() == 2:
            return super().edit(index, trigger, event)
        return False
    
    def on_item_double_clicked(self, item, column):
        """ 树控件子项双击事件 """
        try:
            if item.data(0, Qt.UserRole) == 'module':
                self.item_double_clicked_signal.emit(item.data(1, Qt.UserRole)) # 发送信号
        except AttributeError:
            pass
    
    def dragEnterEvent(self, event):
        """ 
        接受拖拽操作事件，拖动进入组件时触发。
        
        只接受action类子项进入
        """
        # 获取拖动源(因为有跨组件拖拽)
        source = event.source()
        if isinstance(source, QTreeWidget):
            # 通过选择的项来识别被拖动的子项
            dragged_item = source.currentItem()
            dragged_item_type = dragged_item.data(0, Qt.UserRole)
            if dragged_item_type == 'action':
                event.accept()

    def dragMoveEvent(self, event):
        """ 组件内移动事件 """
        item = self.itemAt(event.pos())
        if item:
            can_accept = item.data(3, Qt.UserRole)
            if can_accept:
                event.acceptProposedAction()
            else:
                event.ignore()
        else:
            # 如果没有拖动目标项（即拖动到了空白区域），拒绝拖动操作
            event.ignore()

    def dropEvent(self, event):
        """ 
        放置事件，当拖动放置时触发。 
        
        只有被标记为（可放置）的子项才可放置
        """
        item = self.itemAt(event.pos())
        if item:
            can_accept = item.data(3, Qt.UserRole)
            if can_accept:
                super().dropEvent(event)
            else:
                event.ignore()
        else:
            # 如果没有拖动目标项（即拖动到了空白区域），拒绝拖动操作
            event.ignore()
    
    def show_context_menu(self, pos: QPoint):
        """ 
        树控件子项右键菜单事件 
        
        pos: 事件位置
        """
        # 获取点击的项
        item = self.itemAt(pos)
        if item:
            # 创建上下文菜单
            context_menu = QMenu(self)
            # 创建菜单项
            actionDelete = QAction("删除", self)
            actionMoveUp = QAction("上移", self)
            actionMoveDown = QAction("下移", self)
            # 连接菜单项的触发信号
            # actionDelete.triggered.connect()
            # actionMoveUp.triggered.connect()
            # actionMoveDown.triggered.connect()
            # 将菜单项添加到上下文菜单
            context_menu.addAction(actionDelete)
            context_menu.addAction(actionMoveUp)
            context_menu.addAction(actionMoveDown)
            # 显示上下文菜单
            context_menu.exec(self.viewport().mapToGlobal(pos))
    
    def on_item_changed(self, item, column):
        print(item)
        print(column)
        print(item.text())
    
if __name__ == '__main__':
    app = QApplication([])
    window = EditDock()
    window.show()
    app.exec()