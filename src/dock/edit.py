'''
Author: HDJ
StartDate: please fill in
LastEditTime: 2024-09-07 00:12:05
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
from PySide6.QtWidgets import (
    QApplication, QLabel, QDockWidget, QVBoxLayout, QWidget, QLineEdit, QTreeWidget, QTreeWidgetItem,
    QMenu, QPushButton
    )
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, QPoint, Signal
from ..treeWidgetItem import ActionItem, ModuleItem, TreeWidgetItem

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
        self.operation_btn.clicked.connect(self.operate)

    

    def operate(self):
        """ 开始测试 """
        self.operate_signal.emit('operate')
        

class TreeWidget(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.setColumnCount(3) # 列数
        self.setHeaderLabels(['参数描述', '参数名称', '参数值'])
        self.setDragEnabled(True) # 能否拖拽
        self.setAcceptDrops(True) # 能否放置
        self.setDropIndicatorShown(True) # 是否启用放置指示器
        self.setDefaultDropAction(Qt.MoveAction) # 放置操作 (MoveAction, CopyAction, LinkAction: 创建一个链接或引用)
        # 连接右键菜单事件
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def edit(self, index, trigger, event):
        """ 仅允许编辑第3列的文本 """
        if index.column() == 2:
            return super().edit(index, trigger, event)
        return False
    
    def on_item_changed(self, item, column):
        """
        子项完成编辑

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
            
    
    def find_parent_item(self, item, condition):
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
                
                if isinstance(source, QTreeWidget): # 拖动源为关键字区域
                    print(True)
                    # 通过选择的项来识别被拖动的子项
                    draggedItem = source.currentItem()
                    draggedItemType = draggedItem.data(0, Qt.UserRole)
                    if draggedItemType == 'action':
                        actionPath = draggedItem.data(1, Qt.UserRole) # 获取 action 路径
                        if item.text(0) == '测试步骤': # 放置目标子项类型一
                            newItem = ActionItem(item, data=('action', actionPath, False, True), editable=True, param_editable=True) # 创建一个新的子项
                            self.add_action_to_module(actionPath, modulePath) # 将 action 信息写入 module
                        elif itemType == 'action': # 放置目标子项类型二
                            itemIndex = item.parent().indexOfChild(item)
                            item.parent().insertChild(itemIndex + 1, ActionItem(None, data=('action', actionPath, False, True), editable=True, param_editable=True)) # 在放置目标子项的下方创建同级子项
                            self.add_action_to_module(actionPath, modulePath) # 将 action 信息写入 module
                        # 确认并完成当前的拖放操作
                        event.acceptProposedAction()
            else:
                # 如果组件不接受放置，拒绝拖动操作
                event.ignore()
        else:
            # 如果没有拖动目标项（即拖动到了空白区域），拒绝拖动操作
            event.ignore()
        self.itemChanged.connect(self.on_item_changed) # 重新开启
    
    def add_action_to_module(self, action_file, module_file):
        start_index = action_file.find('action_keywords') # 查找起始位置
        action_RP = action_file[start_index:] # 提取相对路径
        try:
            # 读取源文件内容
            with open(action_file, 'r', encoding='utf-8') as f:
                action_content = yaml.safe_load(f)
            action_content[0] = {'action_RP': action_RP} | action_content[0] #添加相对路径信息，'|' Operator (Python 3.9+)
            # 读取目标文件内容
            with open(module_file, 'r', encoding='utf-8') as f:
                module_content = yaml.safe_load(f)
            # 确保模块内容有 'step' 键
            if 'step' not in module_content:
                module_content['step'] = None
            # 添加源内容到目标文件的 'step' 部分
            if module_content['step'] is None:
                module_content['step'] = action_content
            else:
                module_content['step'] = module_content['step'] + action_content
            # 将更新后的内容写回目标文件
            with open(module_file, 'w', encoding='utf-8') as f:
                yaml.safe_dump(module_content, f, allow_unicode=True, sort_keys=False)

                print(f"源文件内容已成功添加到 {module_file} 的 'step' 部分")

        except FileNotFoundError as e:
            print(f"文件未找到: {e}")
        except yaml.YAMLError as e:
            print(f"YAML 解析错误: {e}")
        except IOError as e:
            print(f"文件操作失败: {e}")
    
    def display_action_details(self, action_path:str):
        """ 
        展示action的详细信息, 仅供预览 
        
        action_path: 由信号携带
        """
        # 关闭事件处理
        # self.itemChanged.disconnect(self.on_item_changed)
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
    
    def display_module_details(self, module_path:str):
        """ 
        展示module的详细信息, 提供编辑交互UI 
        
        module_path: 由信号携带
        """
        # 清空树控件
        self.clear()
        # 创建module子项
        moduleItem = ModuleItem(self, data=('module', module_path))
        # 自动调整所有列的宽度
        self.resizeColumnToContents(0)
        self.resizeColumnToContents(1)
        self.resizeColumnToContents(2)
        # 开启事件处理
        # self.itemChanged.connect(self.on_item_changed)

    def show_context_menu(self, pos: QPoint):
        """ 
        树控件子项右键菜单事件 
        
        pos: 事件位置
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
    
    def delete_item(self, item):
        """
        删除选中的项
        """
        parent = item.parent() or self.invisibleRootItem()
        parent = item.parent()
        index = parent.indexOfChild(item)
        parent.removeChild(item)
        # 文件变动
        moduleItem = self.topLevelItem(0)
        modulePath = moduleItem.data(1, Qt.UserRole)
        with open(modulePath, 'r', encoding='utf-8') as f:
            content = yaml.safe_load(f)
        removed_action = content['step'].pop(index) # 根据子项索引在文件中删除对应位置上的信息
        with open(modulePath, 'w', encoding='utf-8') as f:
            yaml.safe_dump(content, f, allow_unicode=True, sort_keys=False)

    def move_item_up(self, item):
        """
        上移选中的项
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
            # 文件变动
            moduleItem = self.topLevelItem(0)
            modulePath = moduleItem.data(1, Qt.UserRole)
            with open(modulePath, 'r', encoding='utf-8') as f:
                content = yaml.safe_load(f)
            content['step'][index], content['step'][index - 1] = content['step'][index - 1], content['step'][index] # 交换值
            with open(modulePath, 'w', encoding='utf-8') as f:
                yaml.safe_dump(content, f, allow_unicode=True, sort_keys=False)

    def move_item_down(self, item):
        """
        下移选中的项
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
            # 文件变动
            moduleItem = self.topLevelItem(0)
            modulePath = moduleItem.data(1, Qt.UserRole)
            with open(modulePath, 'r', encoding='utf-8') as f:
                content = yaml.safe_load(f)
            content['step'][index], content['step'][index + 1] = content['step'][index + 1], content['step'][index] # 交换值
            with open(modulePath, 'w', encoding='utf-8') as f:
                yaml.safe_dump(content, f, allow_unicode=True, sort_keys=False)

    
if __name__ == '__main__':
    app = QApplication([])
    window = EditDock()
    window.show()
    app.exec()