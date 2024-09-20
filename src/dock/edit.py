'''
Author: HDJ
StartDate: please fill in
LastEditTime: 2024-09-20 00:15:35
FilePath: \pythond:\LocalUsers\Goodnameisfordoggy-Gitee\VATFT\src\dock\edit.py
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
import typing
from PySide6.QtWidgets import (
    QApplication, QLabel, QDockWidget, QVBoxLayout, QWidget, QLineEdit, QTreeWidget, QTreeWidgetItem,
    QMenu, QPushButton
    )
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, QPoint, Signal, Slot

from utils.filter import filter_item
from utils import logger
from src.treeWidgetItem import ActionItem, ModuleItem, TreeWidgetItem
from src.dock.action import ActionDock
LOG = logger.get_logger()


class EditDock(QDockWidget):
    
    # 自定义信号
    operate_signal = Signal(str)

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
        self.setWindowTitle('测试用例编辑区')
        self.setTitleBarWidget(QLabel('   测试用例编辑区'))
        self.__initUI()
    
    def __initUI(self):
        self.center_widget = QWidget(self)
        self.setWidget(self.center_widget)
        center_widget_layout = QVBoxLayout(self.center_widget)
        # 搜索框
        self.search_box = QLineEdit(self)
        self.search_box.setPlaceholderText("请输入搜索项，按Enter搜索")
        self.search_box.textChanged.connect(self.__search_tree_items)
        center_widget_layout.addWidget(self.search_box)
        # 树状控件
        self.tree = TreeWidget()
        center_widget_layout.addWidget(self.tree)
        # 运行按钮
        self.operation_btn = QPushButton(self, text='开始测试')
        center_widget_layout.addWidget(self.operation_btn)
        self.operation_btn.clicked.connect(self.__operate)
    
    def __search_tree_items(self):
        """ 搜索树控件子项，搜索框绑定操作"""
        search_text = self.search_box.text().lower() # 获取搜索框的文本，并转换为小写
        root = self.tree.invisibleRootItem() # 获取根项
        filter_item(root, search_text)
    
    def __operate(self):
        """ 开始测试,按钮绑定操作 """
        self.operate_signal.emit('operate')
        

class TreeWidget(QTreeWidget):
    
    def __init__(self):
        super().__init__()
        self.setColumnCount(3) # 列数
        self.setHeaderLabels(['参数描述', '参数名称', '参数值'])
        self.setDragEnabled(True) # 能否拖拽
        self.setAcceptDrops(True) # 能否放置
        self.setDropIndicatorShown(True) # 是否启用放置指示器
        self.setDefaultDropAction(Qt.CopyAction) # 放置操作 (MoveAction, CopyAction, LinkAction: 创建一个链接或引用)
        # 连接右键菜单事件
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
    
    @typing.override
    def edit(self, index, trigger, event):
        """ 仅允许编辑第3列的文本 """
        if index.column() == 2:
            return super().edit(index, trigger, event)
        return False
    
    def on_item_changed(self, item: TreeWidgetItem, column):
        """
        子项完成编辑, 树控件事件绑定操作

        :param item: 发生变动的子项，即完成编辑的子项
        :param column: 发生变动的列
        """
        if item:
            key = item.text(1)
            newValue = item.text(column)
            # 文件变动
            mouduleItem = self.topLevelItem(0)
            moudulePath = mouduleItem.data(1, Qt.UserRole)
            with open(moudulePath, 'r', encoding='utf-8') as f:
                content = yaml.safe_load(f)
            try:
                if self.find_parent_item(item, lambda item: item.text(0) == '用例信息'):
                    content['info'][key] = newValue
                elif self.find_parent_item(item, lambda item: item.text(0) == '运行设置'):
                    configIndex = item.parent().parent().indexOfChild(item.parent()) # 根据子项关系查找配置项的索引
                    content['config'][configIndex]['params'][key] = newValue
                elif self.find_parent_item(item, lambda item: item.text(0) == '测试步骤'):
                    stepIndex = item.parent().parent().indexOfChild(item.parent()) # 根据子项关系查找步骤的索引
                    content['step'][stepIndex]['params'][key] = newValue
            except IndexError: # 忽略不存在的键的影响
                pass
            with open(moudulePath, 'w', encoding='utf-8') as f:
                yaml.safe_dump(content, f, allow_unicode=True, sort_keys=False)
    
    def find_parent_item(self, item: TreeWidgetItem, condition: typing.Callable):
        """
        从子项开始，向上递归查找符合条件的父项。
        
        :param item: 起始子项
        :param condition: 查找条件的函数，接受 Item 并返回布尔值
        :return: 符合条件的父项，如果没有找到则返回 None
        """
        current_item = item
        while isinstance(current_item, QTreeWidgetItem):
            if condition(current_item):
                return current_item
            current_item = current_item.parent()
        return None
    
    @typing.override
    def dragEnterEvent(self, event):
        """ 
        接受拖拽操作事件，拖动进入组件时触发。
        
        只接受action类子项进入
        """
        # 获取拖动源(因为有跨组件拖拽)
        source = event.source()
        if isinstance(source, QTreeWidget):
            # 通过选择的项来识别被拖动的子项
            draggedItem = source.currentItem()
            draggedItemType = draggedItem.data(0, Qt.UserRole)
            if draggedItemType == 'action':
                event.accept()
    
    @typing.override
    def dragMoveEvent(self, event):
        """ 
        组件内移动事件 
        """
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
    
    @typing.override
    def dropEvent(self, event):
        """ 
        放置事件，当拖动放置时触发。 
        
        只有被标记为（可放置）的子项才可放置
        """
        self.itemChanged.disconnect(self.on_item_changed) # 关闭事件，防止初始化子项时触发
        item = self.itemAt(event.pos())
        itemType = item.data(0, Qt.UserRole)
        modulePath = self.topLevelItem(0).data(1, Qt.UserRole)
        if item:
            can_accept = item.data(3, Qt.UserRole)
            if can_accept:
                # 获取拖动源(因为有跨组件拖拽)
                source = event.source()
                grandparent = source.parent().parent() # 根据 UI 结构获取祖父级组件
                if isinstance(source, QTreeWidget) and isinstance(grandparent, ActionDock): # 拖动源为关键字区域
                    # 通过当前选择的项来识别被拖动的子项
                    draggedItem = source.currentItem()
                    draggedItemType = draggedItem.data(0, Qt.UserRole)
                    if draggedItemType == 'action':
                        actionPath = draggedItem.data(1, Qt.UserRole) # 获取 action 路径
                        if item.text(0) == '测试步骤': # 放置目标项类型一
                            newItem = ActionItem(item, data=('action', actionPath, False, True), editable=True, param_editable=True) # 创建一个新的子项，放置到最后
                            self.add_action_to_module(actionPath, modulePath) # 将 action 信息写入 module
                        elif itemType == 'action': # 放置目标项类型二
                            itemIndex = item.parent().indexOfChild(item)
                            item.parent().insertChild(itemIndex + 1, ActionItem(None, data=('action', actionPath, False, True), editable=True, param_editable=True)) # 在放置目标子项的下方创建同级子项
                            self.add_action_to_module(actionPath, modulePath, itemIndex + 1)
                        # 确认并完成当前的拖放操作
                        event.acceptProposedAction()
                elif isinstance(source, QTreeWidget) and isinstance(grandparent, EditDock): # 拖动源为编辑区域
                    # 通过当前选择的项来识别被拖动的子项
                    draggedItem = source.currentItem()
                    draggedItemType = draggedItem.data(0, Qt.UserRole)
                    if draggedItemType == 'action': # 被允许放置的类型当前只有 action
                        actionPath = draggedItem.data(1, Qt.UserRole)
                        if item.text(0) == '测试步骤': # 放置目标项类型一
                            draggedItemIndex = item.indexOfChild(draggedItem)
                            tempItem = item.takeChild(draggedItemIndex)
                            item.insertChild(0, tempItem) # 在第一项放置
                            tempItem.setFirstColumnSpanned(True)
                            self.delete_actionInfo(draggedItemIndex)
                            self.add_action_to_module(actionPath, modulePath, 0)
                        elif itemType == 'action': # 放置目标项类型二
                            parent = item.parent() # 拖动项与放置目标项同级，故使用相同的父级
                            itemIndex = parent.indexOfChild(item)
                            draggedItemIndex = parent.indexOfChild(draggedItem)
                            tempItem = parent.takeChild(draggedItemIndex) # 拿起拖动项
                            self.delete_actionInfo(draggedItemIndex)
                            # 计算删除拖拽项后，放置目标项的索引
                            if draggedItemIndex < itemIndex: # 拖拽项在放置目标项的上方, 放置目标项此时上移 index - 1
                                itemIndex = itemIndex - 1
                            else: # 拖拽项在放置目标项的下方，放置目标项索引不变
                                itemIndex = itemIndex
                            # 放置子项
                            if draggedItemIndex - itemIndex != 1:
                                parent.insertChild(itemIndex + 1, tempItem) # 在放置目标子项的下方创建同级子项
                                tempItem.setFirstColumnSpanned(True)
                                self.add_action_to_module(actionPath, modulePath, itemIndex + 1)
                            else: # 拖拽项在放置目标项下方，且两项相邻，则交换两项位置
                                parent.insertChild(itemIndex, tempItem) # 在放置目标子项的下方创建同级子项
                                tempItem.setFirstColumnSpanned(True)
                                self.add_action_to_module(actionPath, modulePath, itemIndex)
                        # 确认并完成当前的拖放操作
                        event.acceptProposedAction()

            else:
                # 如果组件不接受放置，拒绝放置操作
                event.ignore()
        else:
            # 如果没有拖动目标项（即拖动到了空白区域），拒绝放置操作
            event.ignore()
        self.itemChanged.connect(self.on_item_changed) # 重新开启
    
    @Slot(str)
    def display_action_details(self, action_path:str):
        """ 
        展示action的详细信息, 仅供预览 
        
        :param action_path: 由信号携带
        """
        # 清空树控件
        self.clear()
        # 创建action子项
        actionItem = ActionItem(self, data=('action', action_path)) # 配置文件(yaml)有列表结构
        # 展开子项
        actionItem.setExpanded(True)
        # 自动调整所有列的宽度
        self.resizeColumnToContents(0)
        self.resizeColumnToContents(1)
        self.resizeColumnToContents(2)
    
    @Slot(str)
    def display_module_details(self, module_path:str):
        """ 
        展示module的详细信息, 提供编辑交互UI 
        
        :param module_path: 由信号携带
        """
        # 清空树控件
        self.clear()
        # 创建module子项
        moduleItem = ModuleItem(self, data=('module', module_path))
        # 自动调整所有列的宽度
        self.resizeColumnToContents(0)
        self.resizeColumnToContents(1)
        self.resizeColumnToContents(2)
    
    def show_context_menu(self, pos: QPoint):
        """ 
        树控件子项右键菜单事件 
        
        :param pos: 事件位置
        """
        # 获取点击的项
        item = self.itemAt(pos)
        if item:
            itemType = item.data(0, Qt.UserRole)
            if itemType == 'action':
                # 创建上下文菜单
                context_menu = QMenu(self)
                # 创建菜单项
                actionDelete = QAction("删除", self)
                actionMoveUp = QAction("上移", self)
                actionMoveDown = QAction("下移", self)
                # 连接菜单项的触发信号
                actionDelete.triggered.connect(lambda: self.delete_item(item))
                actionMoveUp.triggered.connect(lambda: self.move_item_up(item))
                actionMoveDown.triggered.connect(lambda: self.move_item_down(item))
                # 将菜单项添加到上下文菜单
                context_menu.addAction(actionDelete)
                context_menu.addAction(actionMoveUp)
                context_menu.addAction(actionMoveDown)
                # 显示上下文菜单
                context_menu.exec(self.viewport().mapToGlobal(pos))
    
    def add_action_to_module(self, action_file: str, module_file: str, step_index: int | None = None):
        """ 
        将action文件信息添加到module文件, 拖拽放置事件的文件处理操作
        
        :param step_index: 向module文件(step)中插入action的索引
        """
        start_index = action_file.find('action_keywords') # 查找起始位置
        action_RP = action_file[start_index:] # 提取相对路径
        try:
            with open(action_file, 'r', encoding='utf-8') as f:
                action_content = yaml.safe_load(f)
            action_content[0] = {'action_RP': action_RP} | action_content[0] #添加相对路径信息，'|' Operator (Python 3.9+)
            with open(module_file, 'r', encoding='utf-8') as f:
                module_content = yaml.safe_load(f)
            # 确保模块内容有 'step' 键
            if 'step' not in module_content:
                module_content['step'] = None
            # 向 module 文件( step 字段)中插入 action
            if module_content['step'] is None: # 不存在 action 时
                module_content['step'] = action_content
            else: # 存在 action 时
                if isinstance(step_index, int):
                    module_content['step'].insert(step_index, action_content[0])
                else: # 默认插入到最后
                    module_content['step'] = module_content['step'] + action_content
            # 将更新后的内容写回目标文件
            with open(module_file, 'w', encoding='utf-8') as f:
                yaml.safe_dump(module_content, f, allow_unicode=True, sort_keys=False)
                LOG.trace(f'Add action info to the "step" section of the {module_file}')
        except FileNotFoundError as e:
            LOG.warning(f"File not found : {e}")
        except yaml.YAMLError as e:
            LOG.error(f"YAML parse error: {e}")
        except IOError as e:
            LOG.error(f"File IO failed: {e}")
    
    def delete_actionInfo(self, index: int):
        """ 从 module 文件(step)中删除 action 信息"""
        moduleItem = self.topLevelItem(0)
        modulePath = moduleItem.data(1, Qt.UserRole)
        with open(modulePath, 'r', encoding='utf-8') as f:
            content = yaml.safe_load(f)
        removed_action = content['step'].pop(index) # 根据子项索引在文件中删除对应位置上的信息
        with open(modulePath, 'w', encoding='utf-8') as f:
            yaml.safe_dump(content, f, allow_unicode=True, sort_keys=False)
        LOG.trace(f'Action info at "step" index {index} delete successfully at {modulePath}')
    
    def swap_actionInfo(self, index_1: int, index_2: int):
        """ 将 module 文件(step)中两个不同索引的 action 信息交换 """
        moduleItem = self.topLevelItem(0)
        modulePath = moduleItem.data(1, Qt.UserRole)
        with open(modulePath, 'r', encoding='utf-8') as f:
            content = yaml.safe_load(f)
        content['step'][index_1], content['step'][index_2] = content['step'][index_2], content['step'][index_1] # 交换值
        with open(modulePath, 'w', encoding='utf-8') as f:
            yaml.safe_dump(content, f, allow_unicode=True, sort_keys=False)
        LOG.trace(f'Action info at "step" index {index_1} and {index_2} swap successfully at {modulePath}')
    
    def delete_item(self, item: TreeWidgetItem):
        """
        删除选中的项, 菜单操作
        """
        parent = item.parent() or self.invisibleRootItem()
        parent = item.parent()
        index = parent.indexOfChild(item)
        parent.removeChild(item)
        self.delete_actionInfo(index)
    
    def move_item_up(self, item: TreeWidgetItem):
        """
        上移选中的项, 菜单操作
        """
        parent = item.parent() or self.invisibleRootItem()
        index = parent.indexOfChild(item)
        if index > 0: # 第一项不动
            parent.takeChild(index)
            parent.insertChild(index - 1, item)
            self.setCurrentItem(item)  # 重新选中该项
            # 保持action子项所有列合并
            if item.data(0, Qt.UserRole) == 'action':
                item.setFirstColumnSpanned(True)
            self.swap_actionInfo(index, index - 1)
    
    def move_item_down(self, item: TreeWidgetItem):
        """
        下移选中的项, 菜单操作
        """
        parent = item.parent() or self.invisibleRootItem()
        index = parent.indexOfChild(item)
        if index < parent.childCount() - 1: # 最后一项不动
            parent.takeChild(index)
            parent.insertChild(index + 1, item)
            self.setCurrentItem(item)  # 重新选中该项
            # 保持action子项所有列合并
            if item.data(0, Qt.UserRole) == 'action':
                item.setFirstColumnSpanned(True)
            self.swap_actionInfo(index, index + 1)


if __name__ == '__main__':
    app = QApplication([])
    window = EditDock()
    window.show()
    app.exec()