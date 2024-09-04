'''
Author: HDJ
StartDate: please fill in
LastEditTime: 2024-09-04 23:38:05
FilePath: \pythond:\LocalUsers\Goodnameisfordoggy-Gitee\VATFT\src\dock\project.py
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
    QApplication, QWidget, QLabel, QDockWidget, QVBoxLayout, QLineEdit, QTreeWidget, 
    QMenu, QFileDialog
	)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, QPoint, Signal
from ..treeWidgetItem import TreeWidgetItem
from .. import PROJECTS_DIR


class ProjectDock(QDockWidget):
    
    # 自定义信号
    item_double_clicked_signal = Signal(str)  # 信号携带一个字符串参数
    
    def __init__(self, title='', parent=None):
        super().__init__(title, parent)
        self.setWindowTitle('项目')
        self.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetClosable)
        self.initUI()
        self.load_project(r"D:\LocalUsers\Goodnameisfordoggy-Gitee\VATFT\projects\pro")
        
    def initUI(self):
        self.center_widget = QWidget(self)
        self.setWidget(self.center_widget)
        center_widget_layout = QVBoxLayout(self.center_widget)
        

        # 搜索框
        self.search_box = QLineEdit(self)
        self.search_box.setPlaceholderText("请输入搜索项，按Enter搜索")
        # self.search_box.textChanged.connect()
        center_widget_layout.addWidget(self.search_box)

        # 树控件
        self.tree = QTreeWidget()
        center_widget_layout.addWidget(self.tree)
        self.tree.setHeaderHidden(True) # 隐藏表头
        self.tree.itemDoubleClicked.connect(self.on_item_double_clicked)
        # 连接右键菜单事件
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.show_context_menu)

    def select_project(self) -> str:
        directory_path = QFileDialog.getExistingDirectory(self, "选择项目目录", PROJECTS_DIR)
        return directory_path
    
    def load_project(self, directory_path: str):
        """ 加载项目 """
        # 创建树控件子项
        if directory_path:
            projectItem = TreeWidgetItem(self.tree, [os.path.basename(directory_path)], ('project', directory_path))
            first_iteration = True
            for root, dirs, files in os.walk(os.path.join(directory_path, 'business')): # 项目目录下的business()
                if first_iteration:
                    first_iteration = False
                    continue
                packageItem = TreeWidgetItem(projectItem, [os.path.basename(root)], ('packageItem', root))
                for file_name in files:
                    moduleItem = TreeWidgetItem(packageItem, [os.path.splitext(file_name)[0]], ('module', os.path.join(root, file_name)))

    def on_item_double_clicked(self, item, column):
        """ 树控件子项双击事件 """
        try:
            if item.data(0, Qt.UserRole) == 'module':
                self.item_double_clicked_signal.emit(item.data(1, Qt.UserRole)) # 发送信号
        except AttributeError:
            pass
    
    def show_context_menu(self, pos: QPoint):
        """ 
        树控件子项右键菜单事件 
        
        pos: 事件位置
        """
        # 获取点击的项
        item = self.tree.itemAt(pos)
        if item:
            # 创建上下文菜单
            context_menu = QMenu(self)
            # 创建菜单项
            action_edit = QAction("打开文件(目录)", self)
            # 连接菜单项的触发信号
            action_edit.triggered.connect(lambda: self.open_file(item.data(1, Qt.UserRole)))
            # 将菜单项添加到上下文菜单
            context_menu.addAction(action_edit)
            # 显示上下文菜单
            context_menu.exec(self.tree.viewport().mapToGlobal(pos))
        else:
            context_menu = QMenu(self)
            action_edit = QAction("将文件添加到工作区", self)
            action_edit.triggered.connect(self.load_project)
            context_menu.addAction(action_edit)
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
    window = ProjectDock()
    window.show()
    app.exec()