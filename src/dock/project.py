'''
Author: HDJ
StartDate: please fill in
LastEditTime: 2024-09-19 23:36:52
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
import yaml
import shutil
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QDockWidget, QVBoxLayout, QLineEdit, QTreeWidget, QTreeWidgetItem,
    QMenu, QFileDialog
	)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, QPoint, Signal, Slot

from utils.file import open_file
from utils.filter import filter_item
from utils import logger
from src.treeWidgetItem import TreeWidgetItem
from src.dialogBox.input import NameInputDialogBox
from src.dialogBox.reconfirm import ReconfirmDialogBox
from src import PROJECTS_DIR, CONFIG_DIR
LOG = logger.get_logger()


class ProjectDock(QDockWidget):
    
    def __init__(self, title='', parent=None):
        super().__init__(title, parent)
        self.setWindowTitle('项目')
        self.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetClosable)
        self.__initUI()
        self.load_project(r"D:\LocalUsers\Goodnameisfordoggy-Gitee\VATFT\projects\pro")
        
    def __initUI(self):
        self.center_widget = QWidget(self)
        self.setWidget(self.center_widget)
        center_widget_layout = QVBoxLayout(self.center_widget)
        
        # 搜索框
        self.search_box = QLineEdit(self)
        self.search_box.setPlaceholderText("请输入搜索项，按Enter搜索")
        self.search_box.textChanged.connect(self.__search_tree_items)
        center_widget_layout.addWidget(self.search_box)

        # 树控件
        self.tree = TreeWidget(self)
        center_widget_layout.addWidget(self.tree)
        

    def select_project(self) -> str:
        directory_path = QFileDialog.getExistingDirectory(self, "选择项目目录", PROJECTS_DIR)
        return directory_path
    
    @Slot(str)
    def load_project(self, directory_path: str):
        """ 加载项目 """
        # 暂时禁用信号
        self.tree.blockSignals(True)
        # 创建树控件子项
        if directory_path:
            projectItem = TreeWidgetItem(self.tree, [os.path.basename(directory_path)], ('project', directory_path), checkbox=True)
            first_iteration = True
            for root, dirs, files in os.walk(os.path.join(directory_path, 'business')): # 项目目录下的business()
                if first_iteration:
                    first_iteration = False
                    continue
                packageItem = TreeWidgetItem(projectItem, [os.path.basename(root)], ('package', root), checkbox=True)
                for file_name in files:
                    moduleItem = TreeWidgetItem(packageItem, [os.path.splitext(file_name)[0]], ('module', os.path.join(root, file_name)), checkbox=True)
            LOG.info(f'Load project from {directory_path}')
        # 启用信号
        self.tree.blockSignals(False)

    def __search_tree_items(self):
        """ 搜索树控件子项，搜索框绑定操作"""
        search_text = self.search_box.text().lower() # 获取搜索框的文本，并转换为小写
        root = self.tree.invisibleRootItem() # 获取根项
        filter_item(root, search_text)

    def get_checked_modules(self):
        """ 获取所有复选框状态为Checked的module子项，并返回对应的文件路径 """
        checked_items = []
        root = self.tree.invisibleRootItem()  # 获取树的根项
        self.tree.__find_checked_items(root, checked_items)
        print(checked_items)
        return checked_items
    
    @staticmethod
    def new_module_file(path: str):
        """ 
        创建 module 级配置文件 
        
        :param path: 目标文件路径
        """
        if not os.path.exists(path):
            if ProjectDock.paste_file(os.path.join(CONFIG_DIR, 'module_template.yaml'), path, 'COPY'): # 直接使用模版文件初始化
                LOG.success('Test cases have been initialized using the template file')
                return True
            # config_data = {}
            # # 创建并写入 YAML 文件
            # with open(path, 'w') as f:
            #     yaml.dump(config_data, f, default_flow_style=False, allow_unicode=True)
        else:
            LOG.warning('A file with the same name exists in the destination location, and the new operation has been canceled')    
    
    @staticmethod
    def new_package_file(path: str):
        """ 
        创建 package 目录
        
        :param path: 目标目录路径
        """
        if path:
            try:
                os.mkdir(path)
                LOG.success(f'Test cases directory create successfully at {path}')
                return True
            except FileExistsError:
                LOG.warning(f'Directory already exists at {path}')
    
    @staticmethod
    def paste_file(source: str, target: str, pre_event: str = '') -> bool:
        """ 
        粘贴文件 
        
        :param source: 原文件路径
        :param target: 目标位路径
        :param pre_event: CUT | COPY
        """
        if source:
            if os.path.exists(target): # 目标位置存在文件
                LOG.trace('A file with the same name exists at the destination location, pasting has been canceled')
                return
            if os.path.splitext(os.path.basename(source))[1] != os.path.splitext(os.path.basename(target))[1]:
                LOG.warning('Note that source file has a different suffix than target file')
            if not pre_event:
                LOG.trace('Param pre_event should be set to CUT or COPY')
            # 剪切粘贴
            if pre_event == 'CUT': 
                shutil.move(source, target) # 移动文件或目录
                return True
            # 复制粘贴
            elif pre_event == 'COPY': 
                # 拷贝文件或目录
                if os.path.isfile(source):
                    shutil.copy(source, target)
                    LOG.success(f'File copy successfully at {target}')
                    return True
                elif os.path.isdir(source):
                    shutil.copytree(source, target)
                    LOG.success(f'Directory copy successfully at {target}')
                    return True
                else:
                    LOG.error(f'{source} is not a file or directory')
    
    @staticmethod
    def delete_file(path: str) -> bool:
        """" 
        删除文件 
        
        :param path: 目标文件路径
        """
        if os.path.exists(path):  # 检查路径是否存在
            if os.path.isfile(path):
                try:
                    os.remove(path)
                    LOG.success(f"File at '{path}' delete successfully")
                    return True
                except PermissionError:
                    LOG.warning(f"Do not have permission to delete files at {path}")
                except Exception as e:
                    LOG.error(f"An error occurred while deleting a file: {e}")
            elif os.path.isdir(path): # 如果是目录直接删除，不考虑是否为空
                try:
                    shutil.rmtree(path)
                    LOG.success(f"Directory at {path} delete successfully")
                    return True
                except PermissionError:
                    LOG.warning(f"Do not have permission to delete directory at {path}")
                except Exception as e:
                    LOG.error(f"An error occurred while deleting a directory: {e}")
            else:
                LOG.warning(f"{path} does not exist.")
    
    @staticmethod
    def rename_file(path: str, name: str = '') -> str:
        """ 
        重命名文件项或目录项，菜单操作 
        
        :param path: 目标文件路径
        :param name: 要更改的名称
        """
        if os.path.exists(path):  # 检查路径是否存在
            dirname = os.path.dirname(path)
            if os.path.isfile(path): # 文件
                extension = os.path.splitext(os.path.basename(path))[1]
                newPath = os.path.join(dirname, name + extension)
            else: # 目录
                newPath = os.path.join(dirname, name)
            try:
                os.rename(path, newPath)
                LOG.success(f'The file or directory has been successfully renamed to {name} at {newPath}')
                return newPath
            except FileNotFoundError:
                LOG.warning(f'File or directory at {path} not found')
            except PermissionError:
                LOG.warning('Do not have permission to rename file or directory')
            except Exception as e:
                LOG.error(f'An error occurred while renaming a directory or file: {e}')
        else:
            LOG.warning(f"{path} does not exist")

class TreeWidget(QTreeWidget):
    
    # 自定义信号
    item_double_clicked_signal = Signal(str)  # 信号携带一个字符串参数
    
    def __init__(self, parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        self.setHeaderHidden(True) # 隐藏表头
        self.itemDoubleClicked.connect(self.__on_item_double_clicked)
        self.itemChanged.connect(self.__on_item_change)
        # 连接右键菜单事件
        self.setContextMenuPolicy(Qt.CustomContextMenu) # 使用自定义菜单
        self.customContextMenuRequested.connect(self.__show_context_menu)
    
    def __on_item_double_clicked(self, item, column):
        """ 树控件子项双击事件，树控件绑定操作 """
        print('__on_item_double_clicked')
        try:
            if item.data(0, Qt.UserRole) == 'module':
                self.item_double_clicked_signal.emit(item.data(1, Qt.UserRole)) # 发送信号
        except AttributeError:
            pass
    
    def __on_item_change(self, item: TreeWidgetItem, column):
        """ 树控件子项变化处理，树控件绑定操作"""
        # 暂时禁用信号处理，避免递归触发
        self.blockSignals(True)
        
        # 获取当前复选框的状态
        check_state = item.checkState(0)
        self.__update_child_items_check_state(item, check_state)
        self.__update_parent_item_check_state(item)
        # 重新启用信号处理
        self.blockSignals(False)
    
    def __show_context_menu(self, pos: QPoint):
        """ 
        树控件子项右键菜单事件，树控件绑定操作
        
        :pos: 事件位置
        """
        # 获取点击的项
        item = self.itemAt(pos)
        if item:
            itemType = item.data(0, Qt.UserRole)
            if itemType in ('module', 'package'):
                # 创建上下文菜单
                context_menu = QMenu(self)
                # 创建菜单项
                newMenu = QMenu('新建', self)
                newModuleAction = QAction('新建测试用例', self)
                newPackageAction = QAction('新建目录', self)
                openAction = QAction('打开文件(目录)', self)
                copyAction = QAction('复制', self)
                cutAction = QAction('剪切', self)
                pasteAction = QAction('粘贴', self)
                deleteAction = QAction('删除', self)
                renameAction = QAction('重命名', self)

                # 连接菜单项的触发信号
                newModuleAction.triggered.connect(lambda: self.__new_module_item(item))
                newPackageAction.triggered.connect(lambda: self.__new_package_item(item))
                openAction.triggered.connect(lambda: open_file(item.data(1, Qt.UserRole)))
                copyAction.triggered.connect(lambda: self.__copy_item(item))
                cutAction.triggered.connect(lambda: self.__cut_item(item))
                pasteAction.triggered.connect(lambda: self.__paste_item(item))
                deleteAction.triggered.connect(lambda: self.__delete_item(item))
                renameAction.triggered.connect(lambda: self.__rename_item(item))

                # 将菜单项添加到上下文菜单
                context_menu.addMenu(newMenu)
                newMenu.addAction(newModuleAction)
                newMenu.addAction(newPackageAction)
                context_menu.addSeparator()  # 分隔符
                context_menu.addAction(openAction)
                context_menu.addSeparator()  # 分隔符
                context_menu.addAction(copyAction)
                context_menu.addAction(cutAction)
                context_menu.addAction(pasteAction)
                context_menu.addAction(deleteAction)
                context_menu.addAction(renameAction)
                context_menu.exec(self.viewport().mapToGlobal(pos)) # 显示上下文菜单
            elif itemType == 'project':
                # 创建上下文菜单
                context_menu = QMenu(self)
                # 创建菜单项
                newMenu = QMenu('新建', self)
                newModuleAction = QAction('新建测试用例', self)
                newPackageAction = QAction('新建目录', self)
                openAction = QAction('打开文件(目录)', self)
                
                # 连接菜单项的触发信号
                newModuleAction.triggered.connect(lambda: self.__new_module_item(item))
                newPackageAction.triggered.connect(lambda: self.__new_package_item(item))
                openAction.triggered.connect(lambda: open_file(item.data(1, Qt.UserRole)))

                # 将菜单项添加到上下文菜单
                context_menu.addMenu(newMenu)
                newMenu.addAction(newModuleAction)
                newMenu.addAction(newPackageAction)
                context_menu.addSeparator()  # 分隔符
                context_menu.addAction(openAction)
                context_menu.exec(self.viewport().mapToGlobal(pos)) # 显示上下文菜单

        else: # 右击树控件空白处
            context_menu = QMenu(self)
            openAction = QAction("将文件添加到工作区", self)
            openAction.triggered.connect(lambda: self.load_project(self.select_project()))
            context_menu.addAction(openAction)
            context_menu.exec(self.viewport().mapToGlobal(pos))
    
    def __update_child_items_check_state(self, current_item: TreeWidgetItem, check_state: Qt.CheckState):
        """ 递归遍历所有子项，并设置与父项一致的复选框状态 """
        for i in range(current_item.childCount()):
            child_item = current_item.child(i)
            child_item.setCheckState(0, check_state)
            self.__update_child_items_check_state(child_item, check_state)
    
    def __update_parent_item_check_state(self, current_item: TreeWidgetItem):
        """ 递归，向上设置直系父项的复选框状态 """
        parent_item = current_item.parent()
        if isinstance(parent_item, TreeWidgetItem):
            # 统计子项中被选中的个数
            checked_count = sum(parent_item.child(i).checkState(0) == Qt.Checked for i in range(parent_item.childCount()))
            # 带有子项的父级子项共有三种状态
            if checked_count == parent_item.childCount(): # 全部子项被选中
                parent_item.setCheckState(0, Qt.Checked)
            elif checked_count == 0:
                parent_item.setCheckState(0, Qt.Unchecked) # 未有子项选中
            else:
                parent_item.setCheckState(0, Qt.PartiallyChecked) # 部分子项被选中
            self.__update_parent_item_check_state(parent_item)
    
    def find_checked_items(self, current_item: TreeWidgetItem, checked_items: list):
        """ 递归查找所有选中的子项 """
        for i in range(current_item.childCount()):
            child_item = current_item.child(i)
            if child_item.checkState(0) == Qt.Checked:
                checked_items.append(child_item)  # 获取选中的子项的文本
            self.find_checked_items(child_item, checked_items)  # 递归检查子项
    
    def __new_module_item(self, item: TreeWidgetItem):
        """ 创建 module 级子项，菜单操作"""
        itemType = item.data(0, Qt.UserRole)
        itemPath = item.data(1, Qt.UserRole)
        nameInputDialogBox = NameInputDialogBox(self, '新建模版', '请输入新的测试用例名称：')
        if nameInputDialogBox.exec():
            name = nameInputDialogBox.nameInput()
            # 生成目标路径
            if itemType == 'project':
                targetPath = os.path.join(os.path.join(itemPath, 'business'), name + '.yaml')
            elif itemType == 'package':
                targetPath = os.path.join(itemPath, name + '.yaml')
            elif itemType == 'module':
                dirName = os.path.dirname(itemPath)
                targetPath = os.path.join(dirName, name + '.yaml')
            else:
                LOG.critical('This item or item type does not have that functionality')
            # 创建新文件，并创建新子项
            if ProjectDock.new_module_file(targetPath):
                moduleItem = TreeWidgetItem(None, [name], ('module', targetPath))
                if itemType in ('project', 'package'):
                    item.addChild(moduleItem)
                    LOG.trace('Module item create successfully')
                elif itemType == 'module':
                    item.parent().addChild(moduleItem)
                    LOG.trace('Module item create successfully')
                else:
                    LOG.trace('Some errors during module item creating')
    
    def __new_package_item(self, item: TreeWidgetItem):
        """ 创建 package 级子项，菜单操作"""
        itemType = item.data(0, Qt.UserRole)
        itemPath = item.data(1, Qt.UserRole)
        nameInputDialogBox = NameInputDialogBox(self, '新建目录', '请输入新的目录名称：')
        if nameInputDialogBox.exec():
            name = nameInputDialogBox.nameInput()
            # 生成目标路径
            if itemType == 'project':
                targetPath = os.path.join(os.path.join(itemPath, 'business'), name)
            elif itemType == 'package':
                targetPath = os.path.join(itemPath, name)
            elif itemType == 'module':
                dirName = os.path.dirname(itemPath)
                targetPath = os.path.join(dirName, name)
            else:
                LOG.critical('This item or item type does not have that functionality')
            # 创建新目录，并创建新子项
            if ProjectDock.new_package_file(targetPath):
                packageItem = TreeWidgetItem(None, [name], ('package', targetPath))
                if itemType in ('project', 'package'):
                    item.addChild(packageItem)
                    LOG.trace('Package item create successfully')
                elif itemType == 'module':
                    item.parent().addChild(packageItem)
                    LOG.trace('Package item create successfully')
                else:
                    LOG.trace('Some errors during package item creating')
    
    def __copy_item(self, item: TreeWidgetItem):
        """ 复制文件项或目录项，菜单操作 """
        itemPath = item.data(1, Qt.UserRole)
        self.__current_path = itemPath
        self.__tempItem = item
        self.__current_path = False
        LOG.trace(f'Item {item.text(0)} was copied')
    
    def __cut_item(self, item: TreeWidgetItem):
        """ 剪切文件项或目录项，菜单操作 """
        itemPath = item.data(1, Qt.UserRole)
        self.__current_path = itemPath
        self.__tempItem = item
        self.__current_path = True
        LOG.trace(f'Item {item.text(0)} was cut')
    
    def __paste_item(self, item: TreeWidgetItem):
        """ 粘贴文件项或目录项，菜单操作 """
        itemPath = item.data(1, Qt.UserRole)
        itemType = item.data(0, Qt.UserRole)
        try:
            baseName = os.path.basename(self.__current_path)
        except AttributeError: # current_path
            LOG.trace('There is no prior copy or cut, pasting has been canceled')
            return
        # 获取目标路径，只能为目录
        if itemType == 'module':
            targetPath = os.path.join(os.path.dirname(itemPath), baseName)
        else:
            targetPath = os.path.join(itemPath, baseName)
        # 处理原子项
        itemIndex = self.__tempItem.parent().indexOfChild(self.__tempItem)
        if self.__current_path:
            if ProjectDock.paste_file(self.__current_path, targetPath, 'CUT'):
                self.__tempItem = self.__tempItem.parent().takeChild(itemIndex)
        else:
            if ProjectDock.paste_file(self.__current_path, targetPath, 'COPY'):
                self.__tempItem = self.__tempItem.clone() # 一个 QTreeWidgetItem 实例只能属于一个父项, 故重新创建
        # 创建新子项
        self.__tempItem.change_UserData(1, targetPath) # 子项携带的路径信息更改
        if itemType == 'module':
            item.parent().addChild(self.__tempItem)
            LOG.trace('Item paste successfully')
        elif itemType == 'package':
            item.addChild(self.__tempItem)
            LOG.trace('Item paste successfully')
            
        del self.__current_path
        del self.__current_path
    
    def __delete_item(self, item: TreeWidgetItem):
        """ 删除文件项或目录项，菜单操作 """
        itemPath = item.data(1, Qt.UserRole)
        if ReconfirmDialogBox(self, '删除', '确定要删除该文件吗？').exec():
            if ProjectDock.delete_file(itemPath):
                item.parent().removeChild(item)
                LOG.trace('Item delete successfully')

    def __rename_item(self, item: TreeWidgetItem):
        """ 重命名文件项或目录项，菜单操作 """
        itemPath = item.data(1, Qt.UserRole)
        nameInputDialogBox = NameInputDialogBox(self, '重命名', '请输入新的文件名称：')
        nameInputDialogBox.set_default_name(item.text(0))
        if nameInputDialogBox.exec():
            newName = nameInputDialogBox.nameInput()
            newPath = ProjectDock.rename_file(itemPath, newName)
            if newPath:
                item.setText(0, os.path.splitext(os.path.basename(newPath))[0])
                item.change_UserData(1, newPath)
                LOG.trace('Item rename successfully')

if __name__ == '__main__':
    app = QApplication([])
    window = ProjectDock()
    window.show()
    app.exec()