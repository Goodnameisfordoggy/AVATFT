'''
Author: HDJ
StartDate: please fill in
LastEditTime: 2024-09-13 21:55:56
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
    QMenu, QFileDialog, QMessageBox
	)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, QPoint, Signal
from src.treeWidgetItem import TreeWidgetItem
from src.dialogBox.input import NameInputDialogBox
from src.dialogBox.reconfirm import ReconfirmDialogBox
from src import PROJECTS_DIR


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
                renameAction = QAction('重命名', self)

                # 连接菜单项的触发信号
                newModuleAction.triggered.connect(lambda: self.copy_item(item))
                newPackageAction.triggered.connect(lambda: self.copy_item(item))
                openAction.triggered.connect(lambda: self.open_file(item.data(1, Qt.UserRole)))
                copyAction.triggered.connect(lambda: self.copy_item(item))
                cutAction.triggered.connect(lambda: self.cut_item(item))
                pasteAction.triggered.connect(lambda: self.paste_item(item))
                deleteAction.triggered.connect(lambda: self.delete_item(item))
                renameAction.triggered.connect(lambda: self.rename_item(item))

                # 将菜单项添加到上下文菜单
                context_menu.addMenu(newMenu)
                newMenu.addAction(newModuleAction)
                newMenu.addAction(newPackageAction)
                context_menu.addAction(openAction)
                context_menu.addAction(copyAction)
                context_menu.addAction(cutAction)
                context_menu.addAction(pasteAction)
                context_menu.addAction(deleteAction)
                context_menu.addAction(renameAction)
                context_menu.exec(self.tree.viewport().mapToGlobal(pos)) # 显示上下文菜单
        else: # 右击树控件空白处
            context_menu = QMenu(self)
            openAction = QAction("将文件添加到工作区", self)
            openAction.triggered.connect(self.load_project)
            context_menu.addAction(openAction)
            context_menu.exec(self.tree.viewport().mapToGlobal(pos))
        

    def copy_item(self, item: QTreeWidgetItem):
        """ 复制文件项或目录项，菜单操作 """
        itemPath = item.data(1, Qt.UserRole)
        self.current_path = itemPath
        self.tempItem = item
        self.cutEvent = False
        

    def paste_item(self, item: QTreeWidgetItem):
        """ 粘贴文件项或目录项，菜单操作 """
        itemPath = item.data(1, Qt.UserRole)
        itemType = item.data(0, Qt.UserRole)
        try:
            baseName = os.path.basename(self.current_path)
        except AttributeError:
            # current_path 不存在
            return
        # 获取目标路径，只能为目录
        if itemType == 'module':
            targetPath = os.path.join(os.path.dirname(itemPath), baseName)
        else:
            targetPath = os.path.join(itemPath, baseName)
        if self.current_path:
            if os.path.exists(targetPath): # 目标位置存在文件
                return
            # 剪切后的粘贴
            if self.cutEvent: 
                shutil.move(self.current_path, targetPath) # 移动文件或目录
                print(self.tempItem)
                self.tempItem.parent().removeChild(self.tempItem) # 移除子项
            # 复制后的粘贴
            else: 
                # 拷贝文件或目录
                if os.path.isfile(self.current_path):
                    shutil.copy(self.current_path, targetPath)
                elif os.path.isdir(self.current_path):
                    shutil.copytree(self.current_path, targetPath)
                else:
                    raise ValueError(f'路径 {self.current_path} 不是文件也不是目录')
            # 添加子项
            self.tempItem.change_UserData(1, targetPath) # 子项携带的路径信息更改
            if itemType == 'module':
                print(1)
                item.parent().addChild(self.tempItem)
            else:
                print(2)
                print(self.tempItem)
                print(self.tempItem.data(0, Qt.UserRole))
                item.addChild(self.tempItem)

            del self.current_path
            del self.cutEvent

    def cut_item(self, item: QTreeWidgetItem):
        """ 剪切文件项或目录项，菜单操作 """
        itemPath = item.data(1, Qt.UserRole)
        self.current_path = itemPath
        self.tempItem = item
        self.cutEvent = True
    
    def delete_item(self, item: QTreeWidgetItem):
        """ 删除文件项或目录项，菜单操作 """
        itemPath = item.data(1, Qt.UserRole)
        if self.delete_file(itemPath):
            item.parent().removeChild(item)

    def rename_item(self, item: QTreeWidgetItem):
        """ 重命名文件项或目录项，菜单操作 """
        itemPath = item.data(1, Qt.UserRole)
        newName = self.rename_file(itemPath, item.text(0))
        if newName:
            item.setText(0, newName)

    def delete_file(self, path: str) -> bool:
        """" 删除文件 """
        if ReconfirmDialogBox(self, '删除', '确定要删除该文件吗？').exec():
            if os.path.exists(path):  # 检查路径是否存在
                if os.path.isfile(path):
                    try:
                        os.remove(path)
                        print(f"文件 '{path}' 删除成功。")
                        return True
                    except PermissionError:
                        print(f"删除文件的权限被拒绝：'{path}'")
                    except Exception as e:
                        print(f"删除文件时发生错误：{e}")
                elif os.path.isdir(path): # 如果是目录直接删除，不考虑是否为空
                    try:
                        shutil.rmtree(path)
                        print(f"目录 '{path}' 删除成功。")
                        return True
                    except PermissionError:
                        print(f"删除目录的权限被拒绝：'{path}'.")
                    except Exception as e:
                        print(f"删除目录时发生错误：{e}")
            else:
                print(f"'{path}' does not exist.")
    
    def rename_file(self, path: str, default_name: str = '') -> str:
        """ 重命名文件项或目录项，菜单操作 """
        nameInputDialogBox = NameInputDialogBox(self, '重命名', '请输入新的文件名称：')
        if default_name:
            nameInputDialogBox.set_default_name(default_name)
        if nameInputDialogBox.exec():
            if os.path.exists(path):  # 检查路径是否存在
                dirname = os.path.dirname(path)
                newName = nameInputDialogBox.nameInput()
                if os.path.isfile(path):
                    extension = os.path.splitext(os.path.basename(path))[1]
                    newPath = os.path.join(dirname, newName + extension)
                else:
                    newPath = os.path.join(dirname, newName)
                try:
                    os.rename(path, newPath)
                    print(f'文件或目录已成功重命名为: {newPath}')
                    return newName
                except FileNotFoundError:
                    print(f'文件或目录 {path} 未找到')
                except PermissionError:
                    print('权限不足，无法重命名文件或目录')
                except Exception as e:
                    print(f'发生错误: {e}')
            else:
                print(f"'{path}' 不存在。")

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