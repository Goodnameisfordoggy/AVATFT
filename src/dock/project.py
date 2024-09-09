'''
Author: HDJ
StartDate: please fill in
LastEditTime: 2024-09-09 18:52:16
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
import shutil
import subprocess
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QDockWidget, QVBoxLayout, QLineEdit, QTreeWidget, QTreeWidgetItem,
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
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu) # 使用自定义菜单
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
                packageItem = TreeWidgetItem(projectItem, [os.path.basename(root)], ('package', root))
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
            itemType = item.data(0, Qt.UserRole)
            if itemType in ('module', 'package'):
                # 创建上下文菜单
                context_menu = QMenu(self)
                # 创建菜单项
                newMenu = QMenu('新建', self)
                newModuleAction = QAction('新建用例', self)
                newPackageAction = QAction('新建目录', self)
                openAction = QAction('打开文件(目录)', self)
                copyAction = QAction('复制', self)
                cutAction = QAction('剪切', self)
                pasteAction = QAction('粘贴', self)
                deleteAction = QAction('删除', self)

                # 连接菜单项的触发信号
                openAction.triggered.connect(lambda: self.open_file(item.data(1, Qt.UserRole)))
                copyAction.triggered.connect(lambda: self.copy_item(item))
                cutAction.triggered.connect(lambda: self.cut_item(item))
                pasteAction.triggered.connect(lambda: self.paste_item(item))
                deleteAction.triggered.connect(lambda: self.delete_item(item))
                
                # 将菜单项添加到上下文菜单
                context_menu.addMenu(newMenu)
                newMenu.addAction(newModuleAction)
                newMenu.addAction(newPackageAction)
                context_menu.addAction(openAction)
                context_menu.addAction(copyAction)
                context_menu.addAction(cutAction)
                context_menu.addAction(pasteAction)
                context_menu.addAction(deleteAction)
                context_menu.exec(self.tree.viewport().mapToGlobal(pos)) # 显示上下文菜单
        else: # 右击树控件空白处
            context_menu = QMenu(self)
            openAction = QAction("将文件添加到工作区", self)
            openAction.triggered.connect(self.load_project)
            context_menu.addAction(openAction)
            context_menu.exec(self.tree.viewport().mapToGlobal(pos))
        

    def copy_item(self, item: QTreeWidgetItem):
        """ 复制文件或目录, 菜单操作 """
        itemPath = item.data(1, Qt.UserRole)
        self.current_path = itemPath
        itemIndex = item.parent().indexOfChild(item)
        self.tempItem = item.clone()
        
        

    def paste_item(self, item: QTreeWidgetItem):
        """ 粘贴文件或目录, 菜单操作 """
        itemPath = item.data(1, Qt.UserRole)
        itemType = item.data(0, Qt.UserRole)
        baseName = os.path.basename(self.current_path)
        # 获取目标路径，只能为目录
        if itemType == 'module':
            targetPath = os.path.join(os.path.dirname(itemPath), baseName)
            item.parent().addChild(self.tempItem)
        else:
            targetPath = os.path.join(itemPath, baseName)
            item.addChild(self.tempItem)
        print(targetPath)
        if self.current_path:
            if os.path.exists(targetPath): # 目标位置存在文件
                if os.path.samefile(self.current_path, targetPath): # 检测文件是否相同
                    return
            if os.path.isfile(self.current_path):
                shutil.copy(self.current_path, targetPath)
            elif os.path.isdir(self.current_path):
                shutil.copytree(self.current_path, targetPath)
            else:
                raise TypeError
            if itemType == 'module':
                item.parent().addChild(self.tempItem)
            else:
                item.addChild(self.tempItem)
            del self.current_path

    def cut_item(self, item: QTreeWidgetItem):
        """ 剪切文件或目录, 菜单操作 """
        pass
    def delete_item(self, item: QTreeWidgetItem):
        """ 删除文件或目录，菜单操作 """
        pass
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