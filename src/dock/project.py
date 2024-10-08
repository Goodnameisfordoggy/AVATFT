'''
Author: HDJ
StartDate: please fill in
LastEditTime: 2024-10-09 00:01:36
FilePath: \pythond:\LocalUsers\Goodnameisfordoggy-Gitee\AVATFT\src\dock\project.py
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
from PySide6.QtCore import Qt, QPoint, Signal, Slot

from utils.file import open_file
from utils.filter import filter_item
from utils import logger
from src.treeWidgetItem import TreeWidgetItem
from src.dialogBox.input import NameInputDialogBox
from src.dialogBox.reconfirm import ReconfirmDialogBox
from src import PROJECTS_DIR, CONFIG_DIR, ICON_DIR, TEMPLATE_DIR
LOG = logger.get_logger()


class ProjectDock(QDockWidget):
    
    # 自定义信号
    closeSignal = Signal(str)
    operateResponseSignal = Signal(list)
    
    def __init__(self, title='', parent=None):
        super().__init__(title, parent)
        self.setWindowTitle('项目')
        self.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetClosable)
        self.setObjectName('NEUTRAL')
        self.__initUI()
        self.load_history_project()
        
    def __initUI(self):
        self.center_widget = QWidget(self)
        self.setWidget(self.center_widget)
        center_widget_layout = QVBoxLayout(self.center_widget)
        
        # 搜索框
        self.search_box = QLineEdit(self)
        self.search_box.setObjectName('NEUTRAL')
        self.search_box.setPlaceholderText("请输入搜索项，按Enter搜索")
        self.search_box.textChanged.connect(self.__search_tree_items)
        center_widget_layout.addWidget(self.search_box)

        # 树控件
        self.tree = TreeWidget(self)
        center_widget_layout.addWidget(self.tree)
    
    @Slot(str)
    def new_project(self, msg: str):
        """ 创建新工程目录，菜单操作"""
        nameInputDialogBox = NameInputDialogBox(self, '新建工程', '请输入新工程的名称：')
        if nameInputDialogBox.exec():
            projectName = nameInputDialogBox.nameInput() # 要创建的顶级目录名称
            projectPath = os.path.join(PROJECTS_DIR, projectName)
            try:
                # 创建完整的目录结构
                os.makedirs(f"{projectPath}/business")
                os.makedirs(f"{projectPath}/config")
                os.makedirs(f"{projectPath}/data")
                os.makedirs(f"{projectPath}/log")
                LOG.success(f'Project {projectName} create successfully')
            except Exception as err:
                LOG.debug(f'Exception: {err}')
            self.tree.load_project_item(projectPath)

    def select_project(self) -> str:
        directory_path = QFileDialog.getExistingDirectory(self, "选择项目目录", PROJECTS_DIR)
        return directory_path
    
    @Slot(str)
    def load_project(self, directory_path: str):
        """ 加载项目 """
        if directory_path:
            if os.path.isdir(directory_path):
                # 读取历史工程, 若是新工程则加入历史记录
                workspace_file = os.path.join(CONFIG_DIR, 'workspace.json')
                try:
                    with open(workspace_file, 'r') as file:
                        workspace_settings = json.load(file)
                except FileNotFoundError:
                    LOG.critical(f"The file {workspace_file} not exist")
                except json.JSONDecodeError:
                    LOG.error(f"The file {workspace_file} is not valid JSON")
                except Exception as e:
                    LOG.error(f"An error occurred: {e}")
                folders = workspace_settings['folders']
                folder_paths = [folder['path'] for folder in folders]
                if directory_path not in folder_paths:
                    workspace_settings['folders'].append({'path': directory_path})
                    with open(workspace_file, 'w') as file:
                        json.dump(workspace_settings, file, indent=4, ensure_ascii=False)
                    self.tree.load_project_item(directory_path)
                    LOG.info(f'Load project from {directory_path}')
    
    def load_history_project(self):
        """ 从配置文件中载入历史工程 """
        workspace_file = os.path.join(CONFIG_DIR, 'workspace.json')
        try:
            with open(workspace_file, 'r') as file:
                workspace_settings = json.load(file)
        except FileNotFoundError:
            LOG.critical(f"The file {workspace_file} not exist")
        except json.JSONDecodeError:
            LOG.error(f"The file {workspace_file} is not valid JSON")
        except Exception as e:
            LOG.error(f"An error occurred: {e}")

        folders: list[dict] = workspace_settings['folders']
        if folders:
            for folder in folders:
                if os.path.isdir(folder['path']):
                    self.tree.load_project_item(folder['path'])
                    LOG.info(f'Load project from history path "{folder['path']}"')


    def __search_tree_items(self):
        """ 搜索树控件子项，搜索框绑定操作"""
        search_text = self.search_box.text().lower() # 获取搜索框的文本，并转换为小写
        root = self.tree.invisibleRootItem() # 获取根项
        filter_item(root, search_text)
    
    @Slot(str)
    def get_checked_modules(self, msg: str):
        """ 
        获取所有复选框状态为 Checked 的 module 级子项，使用信号将对应的文件路径列表 response
        
        """
        checked_items = []
        root = self.tree.invisibleRootItem()  # 获取树的根项
        self.tree.find_checked_items(root, checked_items)
        modulePaths = [item.path for item in checked_items if item.type == 'Project:module']
        self.operateResponseSignal.emit(modulePaths)
    
    @staticmethod
    def new_module_file(path: str) -> bool:
        """ 
        创建 module 级配置文件 
        
        :param path: 目标文件路径
        """
        if not os.path.exists(path):
            if ProjectDock.paste_file(os.path.join(TEMPLATE_DIR, 'module_template.yaml'), path, 'COPY'): # 直接使用模版文件初始化
                LOG.success('Test cases have been initialized using the template file')
                return True
            # config_data = {}
            # # 创建并写入 YAML 文件
            # with open(path, 'w') as f:
            #     yaml.dump(config_data, f, default_flow_style=False, allow_unicode=True)
        else:
            LOG.warning('A file with the same name exists in the destination location, and the new operation has been canceled')    
    
    @staticmethod
    def new_package_file(path: str) -> bool:
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
        :return: 更改完名称的文件绝对路径
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
    
    @typing.override
    def closeEvent(self, event) -> None:
        self.closeSignal.emit('close')
        return super().closeEvent(event)

class TreeWidget(QTreeWidget):
    
    # 自定义信号
    itemDoubleClickedSignal = Signal(str)  # 信号携带一个字符串参数
    loadProjectSignal = Signal(str)
    
    def __init__(self, parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        self.setObjectName('NEUTRAL') 
        self.setHeaderHidden(True) # 隐藏表头
        self.itemDoubleClicked.connect(self.__on_item_double_clicked)
        self.itemChanged.connect(self.__on_item_change)
        # 连接右键菜单事件
        self.setContextMenuPolicy(Qt.CustomContextMenu) # 使用自定义菜单
        self.customContextMenuRequested.connect(self.__show_context_menu)
    
    def load_project_item(self, directory_path: str):
        """ 创建树控件子项 """
        # 暂时禁用信号
        self.blockSignals(True)
        projectItem = TreeWidgetItem(self, [os.path.basename(directory_path)], ('Project:project', directory_path), checkbox=True)
        self.create_item_by_directory_structure(os.path.join(directory_path, 'business'), projectItem)
        # 启用信号
        self.blockSignals(False)
        
    def find_checked_items(self, current_item: TreeWidgetItem, checked_items: typing.List[TreeWidgetItem | None]):
        """ 递归查找所有被选中的子项 """
        for i in range(current_item.childCount()):
            child_item = current_item.child(i)
            if child_item.checkState(0) == Qt.Checked:
                checked_items.append(child_item)  # 获取选中的子项的文本
            self.find_checked_items(child_item, checked_items)  # 递归检查子项
    
    def create_item_by_directory_structure(self, root_dir: str, parent):
        """ 
        更新子项，根据传入的根目录结构来构建树控件 
        
        :param root_dir: 根目录路径
        :param parent: 根目录所对应的项
        """
        # 获取目录中的所有条目，并按照原始顺序列出
        with os.scandir(root_dir) as it:
            for entry in it:
                # 如果是目录
                if entry.is_dir():
                    newItem = TreeWidgetItem(parent, [entry.name], ('Project:package', entry.path), checkbox=True)
                    # 递归调用，传入新的父项
                    self.create_item_by_directory_structure(entry.path, newItem)
                # 如果是文件
                else:
                    newItem = TreeWidgetItem(parent, [os.path.splitext(entry.name)[0]], ('Project:module', entry.path), checkbox=True)
    
    def __on_item_double_clicked(self, item, column):
        """ 树控件子项双击事件，树控件绑定操作 """
        try:
            if item.type == 'Project:module':
                self.itemDoubleClickedSignal.emit(item.path) # 发送信号
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
            if item.type in ('Project:module', 'Project:package'):
                # 创建上下文菜单
                context_menu = QMenu(self)
                # 创建菜单项
                newMenu = QMenu('新建', self)
                newModuleAction = QAction(QIcon(os.path.join(ICON_DIR, 'file-plus.svg')), '新建测试用例', self)
                newPackageAction = QAction(QIcon(os.path.join(ICON_DIR, 'folder-plus.svg')), '新建目录', self)
                openAction = QAction(QIcon(os.path.join(ICON_DIR, 'folder-eye.svg')), '打开文件(目录)', self)
                copyAction = QAction(QIcon(os.path.join(ICON_DIR, 'content-copy.svg')), '复制', self)
                cutAction = QAction(QIcon(os.path.join(ICON_DIR, 'content-cut.svg')), '剪切', self)
                pasteAction = QAction(QIcon(os.path.join(ICON_DIR, 'content-paste.svg')), '粘贴', self)
                deleteAction = QAction(QIcon(os.path.join(ICON_DIR, 'trash-can-outline.svg')), '删除', self)
                renameAction = QAction(QIcon(os.path.join(ICON_DIR, 'rename.svg')), '重命名', self)

                # 连接菜单项的触发信号
                newModuleAction.triggered.connect(lambda: self.__new_module_item(item))
                newPackageAction.triggered.connect(lambda: self.__new_package_item(item))
                openAction.triggered.connect(lambda: open_file(item.path))
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
            elif item.type == 'Project:project':
                # 创建上下文菜单
                context_menu = QMenu(self)
                # 创建菜单项
                newMenu = QMenu('新建', self)
                newModuleAction = QAction(QIcon(os.path.join(ICON_DIR, 'file-plus.svg')), '新建测试用例', self)
                newPackageAction = QAction(QIcon(os.path.join(ICON_DIR, 'folder-plus.svg')), '新建目录', self)
                openAction = QAction(QIcon(os.path.join(ICON_DIR, 'folder-eye.svg')), '打开文件(目录)', self)
                addProjectAction = QAction(QIcon(os.path.join(ICON_DIR, 'layers-plus.svg')), '将文件添加到工作区', self)
                removeProjectAction = QAction(QIcon(os.path.join(ICON_DIR, 'layers-remove.svg')), '将文件从工作区移除', self)
                # 连接菜单项的触发信号
                newModuleAction.triggered.connect(lambda: self.__new_module_item(item))
                newPackageAction.triggered.connect(lambda: self.__new_package_item(item))
                openAction.triggered.connect(lambda: open_file(item.path))
                addProjectAction.triggered.connect(lambda: self.loadProjectSignal.emit('load project'))
                removeProjectAction.triggered.connect(lambda: self.takeTopLevelItem(self.indexOfTopLevelItem(item)))

                # 将菜单项添加到上下文菜单
                context_menu.addMenu(newMenu)
                newMenu.addAction(newModuleAction)
                newMenu.addAction(newPackageAction)
                context_menu.addSeparator()  # 分隔符
                context_menu.addAction(openAction)
                context_menu.addSeparator()  # 分隔符
                context_menu.addAction(addProjectAction)
                context_menu.addAction(removeProjectAction)
                
                context_menu.exec(self.viewport().mapToGlobal(pos)) # 显示上下文菜单

        else: # 右击树控件空白处
            context_menu = QMenu(self)
            openAction = QAction(QIcon(os.path.join(ICON_DIR, 'layers-plus.svg')), "将文件添加到工作区", self)
            openAction.triggered.connect(lambda: self.loadProjectSignal.emit('load project'))
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
    
    def __find_specific_item_upward(self, root_item: QTreeWidgetItem, condition: typing.Callable[[], bool]) -> (TreeWidgetItem | QTreeWidgetItem | None):
        """
        从子项开始，向上递归查找符合条件的父项。
        
        :param item: 起始子项
        :param condition: 查找条件的函数，接受 Item 并返回布尔值
        :return: 符合条件的父项，如果没有找到则返回 None
        """
        current_item = root_item
        while isinstance(current_item, QTreeWidgetItem):
            if condition(current_item):
                return current_item
            current_item = current_item.parent()
        return None
    
    def __update_directory_item(self, directory_item: TreeWidgetItem):
        """ 更新目录级子项及其下所有子项"""
        if directory_item.type == 'Project:project':
            directory_item.takeChildren() # 移除所有子项
            self.create_item_by_directory_structure(os.path.join(directory_item.path, 'business'), directory_item)
            LOG.trace(f'Project item update successfullys')
        elif directory_item.type == 'Project:package':
            directory_item.takeChildren() # 移除所有子项
            self.create_item_by_directory_structure(directory_item.path, directory_item)
            LOG.trace(f'Package item update successfullys')
        else:
            LOG.trace(f'Update failed, current item type: {directory_item.type} is not project')
    
    def __new_module_item(self, item: TreeWidgetItem):
        """ 创建 module 级子项，菜单操作"""
        nameInputDialogBox = NameInputDialogBox(self, '新建模版', '请输入新的测试用例名称：')
        if nameInputDialogBox.exec():
            name = nameInputDialogBox.nameInput()
            # 生成目标路径
            if item.type == 'Project:project':
                targetPath = os.path.join(os.path.join(item.path, 'business'), name + '.yaml')
            elif item.type == 'Project:package':
                targetPath = os.path.join(item.path, name + '.yaml')
            elif item.type == 'Project:module':
                dirName = os.path.dirname(item.path)
                targetPath = os.path.join(dirName, name + '.yaml')
            else:
                LOG.critical('This item or item type does not have that functionality')
            # 创建新文件，并创建新子项
            if ProjectDock.new_module_file(targetPath):
                moduleItem = TreeWidgetItem(None, [name], ('Project:module', targetPath), checkbox=True)
                if item.type in ('Project:project', 'Project:package'):
                    item.addChild(moduleItem)
                    LOG.trace('Module item create successfully')
                elif item.type == 'Project:module':
                    item.parent().addChild(moduleItem)
                    LOG.trace('Module item create successfully')
                else:
                    LOG.trace('Some errors during module item creating')
                self.__update_directory_item(self.__find_specific_item_upward(moduleItem, lambda item: item.type == 'Project:package' or item.type == 'Project:project'))
    
    def __new_package_item(self, item: TreeWidgetItem):
        """ 创建 package 级子项，菜单操作"""
        nameInputDialogBox = NameInputDialogBox(self, '新建目录', '请输入新的目录名称：')
        if nameInputDialogBox.exec():
            name = nameInputDialogBox.nameInput()
            # 生成目标路径
            if item.type == 'Project:project':
                targetPath = os.path.join(os.path.join(item.path, 'business'), name)
            elif item.type == 'Project:package':
                targetPath = os.path.join(item.path, name)
            elif item.type == 'Project:module':
                dirName = os.path.dirname(item.path)
                targetPath = os.path.join(dirName, name)
            else:
                LOG.critical('This item or item type does not have that functionality')
            # 创建新目录，并创建新子项
            if ProjectDock.new_package_file(targetPath):
                packageItem = TreeWidgetItem(None, [name], ('Project:package', targetPath), checkbox=True)
                if item.type in ('Project:project', 'Project:package'):
                    item.addChild(packageItem)
                    LOG.trace('Package item create successfully')
                elif item.type == 'Project:module':
                    item.parent().addChild(packageItem)
                    LOG.trace('Package item create successfully')
                else:
                    LOG.trace('Some errors during package item creating')
                self.__update_directory_item(self.__find_specific_item_upward(packageItem.parent(), lambda item: item.type == 'Project:package' or item.type == 'Project:project'))
    
    def __copy_item(self, item: TreeWidgetItem):
        """ 复制文件项或目录项，菜单操作 """
        self.__current_path = item.path
        self.__tempItem = item
        self.__cutEvent = False
        LOG.trace(f'Item {item.text(0)} was copied')
    
    def __cut_item(self, item: TreeWidgetItem):
        """ 剪切文件项或目录项，菜单操作 """
        self.__current_path = item.path
        self.__tempItem = item
        self.__cutEvent = True
        LOG.trace(f'Item {item.text(0)} was cut')
    
    def __paste_item(self, item: TreeWidgetItem):
        """ 粘贴文件项或目录项，菜单操作 """
        try:
            baseName = os.path.basename(self.__current_path)
        except AttributeError: # current_path
            LOG.trace('There is no prior copy or cut, pasting has been canceled')
            return
        # 获取目标路径，只能为目录
        if item.type == 'Project:module':
            targetPath = os.path.join(os.path.dirname(item.path), baseName)
        else:
            targetPath = os.path.join(item.path, baseName)
        # 处理原子项
        itemIndex = self.__tempItem.parent().indexOfChild(self.__tempItem)
        if self.__cutEvent:
            if ProjectDock.paste_file(self.__current_path, targetPath, 'CUT'):
                self.__tempItem = self.__tempItem.parent().takeChild(itemIndex)
        else:
            if ProjectDock.paste_file(self.__current_path, targetPath, 'COPY'):
                self.__tempItem = self.__tempItem.clone() # 一个 QTreeWidgetItem 实例只能属于一个父项, 故重新创建
        # 创建新子项
        self.__tempItem.change_UserData(1, targetPath) # 子项携带的路径信息更改
        if item.type == 'Project:module':
            item.parent().addChild(self.__tempItem)
            LOG.trace('Item paste successfully')
        elif item.type == 'Project:package':
            item.addChild(self.__tempItem)
            LOG.trace('Item paste successfully')
        self.__update_directory_item(self.__find_specific_item_upward(self.__tempItem, lambda item: item.type == 'Project:package' or item.type == 'Project:project'))
        del self.__current_path
        del self.__cutEvent
    
    def __delete_item(self, item: TreeWidgetItem):
        """ 删除文件项或目录项，菜单操作 """
        if ReconfirmDialogBox(self, '删除', '确定要删除该文件吗？').exec():
            if ProjectDock.delete_file(item.path):
                item.parent().removeChild(item)
                LOG.trace('Item delete successfully')

    def __rename_item(self, item: TreeWidgetItem):
        """ 重命名文件项或目录项，菜单操作 """
        nameInputDialogBox = NameInputDialogBox(self, '重命名', '请输入新的文件名称：')
        nameInputDialogBox.set_default_name(item.text(0))
        if nameInputDialogBox.exec():
            newName = nameInputDialogBox.nameInput()
            newPath = ProjectDock.rename_file(item.path, newName)
            if newPath:
                item.setText(0, os.path.splitext(os.path.basename(newPath))[0])
                item.change_UserData(1, newPath)
                LOG.trace('Item rename successfully')
                self.__update_directory_item(self.__find_specific_item_upward(item, lambda item: item.type == 'Project:package' or item.type == 'Project:project'))
