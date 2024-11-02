'''
Author: HDJ
StartDate: please fill in
LastEditTime: 2024-11-02 23:24:46
FilePath: \pythond:\LocalUsers\Goodnameisfordoggy-Gitee\AVATFT\src\controllers\project_controller.py
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
from src.modules.project_module import *
from src.treeWidgetItem import TreeWidgetItem
from src.views import NameInputDialogBox, ReconfirmDialogBox
from src import PROJECTS_DIR, CONFIG_DIR, ICON_DIR
from src.modules.logger import get_global_logger
LOG = get_global_logger()

class ProjectController(QObject):
    
    def __init__(self, project_dock):
        from src.views import ProjectDock
        self.view: ProjectDock = project_dock
        self.__init_connections()
        self.__connect_custom_signals()

    def __init_connections(self):
        """连接内置事件信号与槽函数"""
        self.view.search_box.textChanged.connect(self.__search_tree_items)
        self.view.tree.itemDoubleClicked.connect(self.__on_item_double_clicked)
        self.view.tree.itemChanged.connect(self.__on_item_change)
        self.view.tree.customContextMenuRequested.connect(self.__show_context_menu)

    def __connect_custom_signals(self):
        """连接自定义信号与槽函数"""
        self.view.distorySignal.connect(self.__save_items_expanded_state)
        self.view.loadProjectSignal.connect(lambda: self.__load_project(self.__select_project()))
        self.view.loadHistoryProjectSiganl.connect(self.__load_history_project)
        self.view.newProjectSignal.connect(self.__new_project)
        
    @Slot()
    def __search_tree_items(self):
        """搜索树控件子项，搜索框绑定操作"""
        search_text = self.view.search_box.text().lower() # 获取搜索框的文本，并转换为小写
        root = self.tree.invisibleRootItem() # 获取根项
        filter_item(root, search_text)
    
    @Slot(TreeWidgetItem, int)
    def __on_item_double_clicked(self, item: TreeWidgetItem, column):
        """ 树控件子项双击事件，树控件绑定操作 """
        try:
            if item.type == 'Project:module':
                self.view.itemDoubleClickedSignal.emit(item.path) # 发送信号
        except AttributeError:
            pass
    
    @Slot(TreeWidgetItem, int)
    def __on_item_change(self, item: TreeWidgetItem, column):
        """ 树控件子项变化处理，树控件绑定操作"""
        # 暂时禁用信号处理，避免递归触发
        self.view.tree.blockSignals(True)
        # 获取当前复选框的状态
        check_state = item.checkState(0)
        self.view.update_child_items_check_state(item, check_state)
        self.view.update_parent_item_check_state(item)
        # 重新启用信号处理
        self.view.tree.blockSignals(False)
    
    @ Slot()
    def __show_context_menu(self, pos: QPoint):
        """ 
        树控件子项右键菜单事件，树控件绑定操作
        
        :pos: 事件位置
        """
        # 获取点击的项
        item = self.view.tree.itemAt(pos)
        if item:
            if item.type in ('Project:module', 'Project:package'):
                # 创建上下文菜单
                context_menu = QMenu(self.view.tree)
                # 创建菜单项
                newMenu = QMenu(self.tr("新建"), self.view.tree)
                newModuleAction = QAction(QIcon(os.path.join(ICON_DIR, 'file-plus.svg')), self.tr("新建测试用例", "menu_action_new_module"), self.view.tree)
                newPackageAction = QAction(QIcon(os.path.join(ICON_DIR, 'folder-plus.svg')), self.tr("新建目录", "menu_action_new_package"), self.view.tree)
                openAction = QAction(QIcon(os.path.join(ICON_DIR, 'folder-eye.svg')), self.tr("打开文件(目录)", "menu_action_open_file_or_directory"), self.view.tree)
                copyAction = QAction(QIcon(os.path.join(ICON_DIR, 'content-copy.svg')), self.tr("复制", "menu_action_copy"), self.view.tree)
                cutAction = QAction(QIcon(os.path.join(ICON_DIR, 'content-cut.svg')), self.tr("剪切", "meun_action_cut"), self.view.tree)
                pasteAction = QAction(QIcon(os.path.join(ICON_DIR, 'content-paste.svg')), self.tr("粘贴", "meun_action_paste"), self.view.tree)
                deleteAction = QAction(QIcon(os.path.join(ICON_DIR, 'trash-can-outline.svg')), self.tr("删除", "menu_action_delete"), self.view.tree)
                renameAction = QAction(QIcon(os.path.join(ICON_DIR, 'rename.svg')), self.tr("重命名", "menu_action_rename"), self.view.tree)

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
                context_menu.exec(self.view.tree.viewport().mapToGlobal(pos)) # 显示上下文菜单
            elif item.type == 'Project:project':
                # 创建上下文菜单
                context_menu = QMenu(self.view.tree)
                # 创建菜单项
                newMenu = QMenu(self.tr("新建"), self.view.tree)
                newModuleAction = QAction(QIcon(os.path.join(ICON_DIR, 'file-plus.svg')), self.tr("新建测试用例", "menu_action_new_module"), self.view.tree)
                newPackageAction = QAction(QIcon(os.path.join(ICON_DIR, 'folder-plus.svg')), self.tr("新建目录", "menu_action_new_package"), self.view.tree)
                openAction = QAction(QIcon(os.path.join(ICON_DIR, 'folder-eye.svg')), self.tr("打开文件(目录)", "menu_action_open_file_or_directory"), self.view.tree)
                addProjectAction = QAction(QIcon(os.path.join(ICON_DIR, 'layers-plus.svg')), self.tr("将文件添加到工作区", "menu_action_add_project"), self.view.tree)
                removeProjectAction = QAction(QIcon(os.path.join(ICON_DIR, 'layers-remove.svg')), self.tr("将文件从工作区移除", "menu_action_remove_project"), self.view.tree)
                # 连接菜单项的触发信号
                newModuleAction.triggered.connect(lambda: self.__new_module_item(item))
                newPackageAction.triggered.connect(lambda: self.__new_package_item(item))
                openAction.triggered.connect(lambda: open_file(item.path))
                addProjectAction.triggered.connect(lambda: self.view.loadProjectSignal.emit('load project'))
                removeProjectAction.triggered.connect(lambda: self.__remove_project(self.view.tree.indexOfTopLevelItem(item)))

                # 将菜单项添加到上下文菜单
                context_menu.addMenu(newMenu)
                newMenu.addAction(newModuleAction)
                newMenu.addAction(newPackageAction)
                context_menu.addSeparator()  # 分隔符
                context_menu.addAction(openAction)
                context_menu.addSeparator()  # 分隔符
                context_menu.addAction(addProjectAction)
                context_menu.addAction(removeProjectAction)
                
                context_menu.exec(self.view.tree.viewport().mapToGlobal(pos)) # 显示上下文菜单

        else: # 右击树控件空白处
            context_menu = QMenu(self.view.tree)
            openAction = QAction(QIcon(os.path.join(ICON_DIR, 'layers-plus.svg')), self.tr("将文件添加到工作区", "menu_action_add_project"), self.view.tree)
            openAction.triggered.connect(lambda: self.view.loadProjectSignal.emit('load project'))
            context_menu.addAction(openAction)
            context_menu.exec(self.view.tree.viewport().mapToGlobal(pos))
    
    @Slot(str)
    def __new_project(self, msg: str):
        """ 创建新工程目录，菜单操作"""
        nameInputDialogBox = NameInputDialogBox(self.view, self.tr("新建工程", "dialog_title"), self.tr("请输入新工程的名称：", "dialog_text"))
        if nameInputDialogBox.exec():
            projectName = nameInputDialogBox.nameInput() # 要创建的顶级目录名称
            projectPath = os.path.join(PROJECTS_DIR, projectName)
            try:
                # 创建完整的目录结构
                os.makedirs(f"{projectPath}/business")
                os.makedirs(f"{projectPath}/config")
                os.makedirs(f"{projectPath}/data")
                os.makedirs(f"{projectPath}/log")
                LOG.success(self.tr("项目 '{}' 创建成功", "Log_msg").format(projectName))
            except Exception as err:
                LOG.debug(f'Exception: {err}')
            self.__load_project_item(projectPath)
    
    @Slot(str)
    def __load_project(self, directory_path: str):
        """ 加载项目 """
        if directory_path:
            if os.path.isdir(directory_path):
                # 读取历史工程, 若是新工程则加入历史记录
                workspace_settings = load_file_content(os.path.join(CONFIG_DIR, 'workspace.json'), LOG, translater=True)
                folders = workspace_settings['folders']
                folder_paths = [folder['path'] for folder in folders]
                if directory_path not in folder_paths:
                    workspace_settings['folders'].append({'path': directory_path})
                    save_file_content(os.path.join(CONFIG_DIR, 'workspace.json'), workspace_settings, LOG, translater=True)
                    self.__load_project_item(directory_path)
                    LOG.info(self.tr("从 {} 加载工程", "Log_msg").format(directory_path))
    
    @Slot()
    def __load_history_project(self):
        """ 从配置文件中载入历史工程 """
        workspace_settings = load_file_content(os.path.join(CONFIG_DIR, 'workspace.json'), LOG, translater=True)
        folders: list[dict] = workspace_settings['folders']
        if folders:
            for index, folder in enumerate(folders):
                if os.path.isdir(folder['path']):
                    self.__load_project_item(folder['path'])
                    LOG.info(self.tr("从历史记录中载入工程: {}", "Log_msg").format(folder['path']))
                else:
                    # 移除不合法的目录
                    folders = [folder for folder in folders if os.path.isdir(folder['path'])]
        # 更新历史记录
        workspace_settings['folders'] = folders
        save_file_content(os.path.join(CONFIG_DIR, 'workspace.json'), workspace_settings, LOG, translater=True)
    
    @Slot(str)
    def __get_checked_modules(self, msg: str):
        """ 
        获取所有复选框状态为 Checked 的 module 级子项，使用信号将对应的文件路径列表 response
        
        """
        checked_items = []
        root = self.view.tree.invisibleRootItem()  # 获取树的根项
        self.__find_checked_items(root, checked_items)
        modulePaths = [item.path for item in checked_items if item.type == 'Project:module']
        self.view.operateResponseSignal.emit(modulePaths)

    @Slot()
    def __save_items_expanded_state(self):
        """ 将树子项的展开状态保存到配置文件 """
        workspace_settings = load_file_content(os.path.join(CONFIG_DIR, 'workspace.json'), logger=LOG, translater=True)
        tree_items_expanded_state = {}
        self.__get_items_expanded_state(self.view.tree.invisibleRootItem(), tree_items_expanded_state) # 从树根项开始递归获取每一项的展开状态，并保存到字典中
        workspace_settings['projectAreaExpandedState'] = tree_items_expanded_state
        save_file_content(os.path.join(CONFIG_DIR, 'workspace.json'), workspace_settings, logger=LOG, translater=True)

    def __remove_project(self, index: int):
        """ 移除工程目录， 菜单操作"""
        workspace_setting_file = os.path.join(CONFIG_DIR, 'workspace.json')
        workspace_settings = load_file_content(workspace_setting_file, LOG, True)
        folders: list = workspace_settings['folders']
        workspace_settings['folders'].pop(index)
        self.view.tree.takeTopLevelItem(index)
        save_file_content(workspace_setting_file, workspace_settings, LOG, True)
    
    def update_child_items_check_state(self, current_item: TreeWidgetItem, check_state: Qt.CheckState):
        """ 递归遍历所有子项，并设置与父项一致的复选框状态 """
        for i in range(current_item.childCount()):
            child_item = current_item.child(i)
            child_item.setCheckState(0, check_state)
            self.update_child_items_check_state(child_item, check_state)
    
    def update_parent_item_check_state(self, current_item: TreeWidgetItem):
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
            self.update_parent_item_check_state(parent_item)
    
    def __find_specific_item_upward(self, root_item: QTreeWidgetItem, condition: typing.Callable[[], bool]) -> (TreeWidgetItem | QTreeWidgetItem | None):
        """
        从子项开始，向上递归查找符合条件的首个父项。
        
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
            self.__create_item_by_directory_structure_wrapper(os.path.join(directory_item.path, 'business'), directory_item)
            LOG.trace(f'Project item update successfullys')
        elif directory_item.type == 'Project:package':
            directory_item.takeChildren() # 移除所有子项
            self.__create_item_by_directory_structure_wrapper(directory_item.path, directory_item)
            LOG.trace(f'Package item update successfullys')
        else:
            LOG.trace(f'Update failed, current item type: {directory_item.type} is not project')
    
    def __new_module_item(self, item: TreeWidgetItem):
        """ 创建 module 级子项，菜单操作"""
        nameInputDialogBox = NameInputDialogBox(self.view, self.tr("新建模版", "dialog_title"), self.tr("请输入新的测试用例名称：", "dialog_text"))
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
                LOG.trace('This item or item type does not have that functionality')
            # 创建新文件，并创建新子项
            if new_module_file(targetPath):
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
        nameInputDialogBox = NameInputDialogBox(self.view, self.tr("新建目录", "dialog_title"), self.tr("请输入新的目录名称：", "dialog_text"))
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
                LOG.trace('This item or item type does not have that functionality')
            # 创建新目录，并创建新子项
            if new_package_file(targetPath):
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
            if paste_file(self.__current_path, targetPath, 'CUT'):
                self.__tempItem = self.__tempItem.parent().takeChild(itemIndex)
        else:
            if paste_file(self.__current_path, targetPath, 'COPY'):
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
        if ReconfirmDialogBox(self.view, self.tr("删除", "dialog_title"), self.tr("确定要删除该文件吗？", "dialog_text")).exec():
            if delete_file(item.path):
                item.parent().removeChild(item)
                LOG.trace('Item delete successfully')

    def __rename_item(self, item: TreeWidgetItem):
        """ 重命名文件项或目录项，菜单操作 """
        nameInputDialogBox = NameInputDialogBox(self.view, self.tr("重命名", "dialog_title"), self.tr("请输入新的文件名称：", "dialog_text"))
        nameInputDialogBox.set_default_name(item.text(0))
        if nameInputDialogBox.exec():
            newName = nameInputDialogBox.nameInput()
            newPath = rename_file(item.path, newName)
            if newPath:
                item.setText(0, os.path.splitext(os.path.basename(newPath))[0])
                item.change_UserData(1, newPath)
                LOG.trace('Item rename successfully')
                self.__update_directory_item(self.__find_specific_item_upward(item, lambda item: item.type == 'Project:package' or item.type == 'Project:project'))
    
    def __load_project_item(self, directory_path: str):
        """ 创建树控件子项 """
        # 读取设置
        workspace_settings: dict  = load_file_content(os.path.join(CONFIG_DIR, 'workspace.json'), LOG, translater=True)
        projectAreaExpandedState: dict = workspace_settings['projectAreaExpandedState']
        # 暂时禁用信号
        self.view.tree.blockSignals(True)
        # 创建各级子项
        projectItem = TreeWidgetItem(self.view.tree, [os.path.basename(directory_path)], ('Project:project', directory_path), checkbox=True)
        projectItem_expanded_state = projectAreaExpandedState.get(directory_path)
        if projectItem_expanded_state is not None:
            projectItem.setExpanded(projectItem_expanded_state)
        self.__create_item_by_directory_structure_wrapper(os.path.join(directory_path, 'business'), projectItem)
        # 启用信号
        self.view.tree.blockSignals(False)

    def __select_project(self) -> str:
        directory_path = QFileDialog.getExistingDirectory(self.view, self.tr("选择项目目录", "dialog_title"), PROJECTS_DIR)
        return directory_path
    
    def __find_checked_items(self, current_item: TreeWidgetItem, checked_items: list[TreeWidgetItem | None]):
        """ 递归查找所有被选中的子项 """
        for i in range(current_item.childCount()):
            child_item = current_item.child(i)
            if child_item.checkState(0) == Qt.Checked:
                checked_items.append(child_item)  # 获取选中的子项的文本
            self.__find_checked_items(child_item, checked_items)  # 递归检查子项
        
    def __get_items_expanded_state(self, current_item: TreeWidgetItem, items_expanded_state: dict):
        """ 递归获取所有子项的展开状态 """
        for i in range(current_item.childCount()):
            child_item = current_item.child(i)
            if child_item:
                items_expanded_state[child_item.path] = child_item.isExpanded()
            self.__get_items_expanded_state(child_item, items_expanded_state)  # 递归检查子项
    
    def __create_item_by_directory_structure_wrapper(self, root_dir: str, parent, **kwargs):
        """ 包装函数 """
        # 读取设置
        workspace_settings = load_file_content(os.path.join(CONFIG_DIR, 'workspace.json'), LOG, translater=True)
        projectAreaExpandedState: dict = workspace_settings['projectAreaExpandedState']
        # 调用递归函数
        self.__create_item_by_directory_structure(root_dir, parent, items_expanded_state=projectAreaExpandedState)
    
    def __create_item_by_directory_structure(self, root_dir: str, parent, **kwargs):
        """ 
        创建各级子项，根据传入的根目录结构来构建树控件 
        
        :param root_dir: 根目录路径
        :param parent: 根目录所对应的项

        kwargs:
            items_expanded_state (dict) 储存各级子项展开状态的字典
        """
        items_expanded_state = kwargs.get("items_expanded_state", None)
        # 获取目录中的所有条目，并按照原始顺序列出
        with os.scandir(root_dir) as it:
            for entry in it:
                # 如果是目录
                if entry.is_dir():
                    newItem = TreeWidgetItem(parent, [entry.name], ('Project:package', entry.path), checkbox=True)
                    newItem_expanded_state = items_expanded_state.get(entry.path, None)
                    if newItem_expanded_state is not None:
                        newItem.setExpanded(newItem_expanded_state)
                    # 递归调用，传入新的父项
                    self.__create_item_by_directory_structure(entry.path, newItem, **kwargs)
                # 如果是文件
                else:
                    newItem = TreeWidgetItem(parent, [os.path.splitext(entry.name)[0]], ('Project:module', entry.path), checkbox=True)