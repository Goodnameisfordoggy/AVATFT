'''
Author: HDJ
StartDate: please fill in
LastEditTime: 2024-11-04 22:33:27
FilePath: \pythond:\LocalUsers\Goodnameisfordoggy-Gitee\AVATFT\src\views\dock\edit.py
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
import threading
from PySide6.QtWidgets import (
    QLabel, QDockWidget, QWidget, QLineEdit, QTreeWidget, QTreeWidgetItem, QPushButton, 
    QHBoxLayout, QVBoxLayout, QComboBox, QCheckBox
    )
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, Signal, Slot

from src.modules import load_file_content, save_file_content, identify_input_type
from src.views.tree import TreeWidgetItem, ActionItem
from src.modules.funcs import *
from src import ICON_DIR
from src.modules.logger import get_global_logger
LOG = get_global_logger()

OPERATE_LOCK = threading.Lock()

class EditDock(QDockWidget):
    
    # 自定义信号
    closeSignal = Signal(str)
    displayActionDetailsSignal = Signal(str)
    displayModuleDetailsSignal = Signal(str)
    operateSignal = Signal(list)
    operateRequestSignal = Signal(object)
    isLockEditDockCheckBoxSignal = Signal(bool)
    

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
        self.setWindowTitle(self.tr("测试用例编辑区", "window_title"))
        self.setTitleBarWidget(QLabel(''))
        self.setObjectName('SECONDARY')
        self.setupUi()

    def setupUi(self):
        self.center_widget = QWidget(self)
        self.setWidget(self.center_widget)
        self.center_widget_layout = QVBoxLayout(self.center_widget)

        self.search_layout = QHBoxLayout()
        # 复选框
        self.check_box = QCheckBox(self)
        self.check_box.setObjectName('SECONDARY')
        self.check_box.setEnabled(False)
        self.check_box.setIcon(QIcon(os.path.join(ICON_DIR, 'arrow-collapse-vertical.svg')))
        self.search_layout.addWidget(self.check_box, 1)

        # 复选框
        self.check_box2 = QCheckBox(self)
        self.check_box2.setObjectName('SECONDARY')
        self.check_box2.setEnabled(False)
        self.check_box2.setIcon(QIcon(os.path.join(ICON_DIR, 'arrow-collapse-vertical.svg')))
        self.search_layout.addWidget(self.check_box2, 1)

        # 搜索框
        self.search_box = QLineEdit(self)
        self.search_box.setObjectName('SECONDARY')
        self.search_box.setPlaceholderText(self.tr("请输入搜索项，按Enter搜索", "search_box_placeholder_text"))
        self.search_layout.addWidget(self.search_box, 99)

        # 搜索方法下拉列表
        self.search_combo_box =  QComboBox()
        self.search_combo_box.addItems([self.tr("匹配参数描述", "search_combo_box_item_Pdescribe"), 
                                        self.tr("匹配参数名称", "search_combo_box_item_Pname"), 
                                        self.tr("匹配参数值", "search_combo_box_item_Pvalue")]) # 添加选项
        self.search_layout.addWidget(self.search_combo_box, 1)
        self.center_widget_layout.addLayout(self.search_layout)

        # 树状控件
        self.tree = TreeWidget(self)
        self.tree.setObjectName('SECONDARY')
        self.tree.setColumnCount(3) # 列数
        self.tree.setHeaderLabels([self.tr("参数描述", "search_combo_box_item_Pdescribe"), 
                            self.tr("参数名称", "search_combo_box_item_Pname"), 
                            self.tr("参数值", "search_combo_box_item_Pvalue")])
        self.tree.setDragEnabled(True) # 能否拖拽
        self.tree.setAcceptDrops(True) # 能否放置
        self.tree.setDropIndicatorShown(True) # 是否启用放置指示器
        self.tree.setDefaultDropAction(Qt.CopyAction) # 放置操作 (MoveAction, CopyAction, LinkAction: 创建一个链接或引用)
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu) # 右键菜单
        self.center_widget_layout.addWidget(self.tree)

        self.button_layout = QHBoxLayout()
        # 运行按钮
        self.operation_btn = QPushButton(self, text=self.tr("开始测试", "operation_button_text"))
        self.operation_btn.setFocusPolicy(Qt.NoFocus)  # 禁用键盘焦点
        self.button_layout.addWidget(self.operation_btn)
        self.center_widget_layout.addLayout(self.button_layout)
    
    @typing.override
    def closeEvent(self, event) -> None:
        self.closeSignal.emit('close')
        return super().closeEvent(event)


class TreeWidget(QTreeWidget):
    
    def __init__(self, parent):
        super().__init__(parent) 
        
    @Slot()
    def on_item_changed(self, item: TreeWidgetItem, column):
        """
        子项完成编辑, 树控件事件绑定操作。

        :param item: 发生变动的子项，即完成编辑的子项
        :param column: 发生变动的列
        """
        LOG.debug("on_item_changed")
        if item:
            key = item.text(1)
            newValue = item.text(column)
            newValue = identify_input_type(newValue)
            if newValue is None:
                item.setText(column, "None")
            # 文件变动
            mouduleItem = self.topLevelItem(0)
            content = load_file_content(mouduleItem.path, LOG, translater=True)
            try:
                if self.__find_specific_item_upward(item, lambda item: item.text(0) == self.tr("用例信息")):
                    content['info'][key] = newValue
                elif self.__find_specific_item_upward(item, lambda item: item.text(0) == self.tr("运行设置")):
                    configIndex = item.parent().parent().indexOfChild(item.parent()) # 根据子项关系查找配置项的索引
                    content['config'][configIndex]['params'][key] = newValue
                elif self.__find_specific_item_upward(item, lambda item: item.text(0) == self.tr("测试步骤")):
                    stepIndex = item.parent().parent().indexOfChild(item.parent()) # 根据子项关系查找步骤的索引
                    content['step'][stepIndex]['params'][key] = newValue
            except IndexError: # 忽略不存在的键的影响
                pass
            save_file_content(mouduleItem.path, content, logger=LOG, translater=True)
    
    def __find_specific_item_upward(self, root_item: QTreeWidgetItem, condition: typing.Callable) -> (TreeWidgetItem | QTreeWidgetItem | None):
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
    
    def __add_action_to_module(self, action_file: str, module_file: str, step_index: int | None = None):
        """ 
        将action文件信息添加到module文件, 拖拽放置事件的文件处理操作
        
        :param step_index: 向module文件(step)中插入action的索引
        """
        start_index = action_file.find('action_keywords') # 查找起始位置
        action_RP = action_file[start_index:] # 提取相对路径
        action_content = load_file_content(action_file, logger=LOG, translater=True)
        module_content = load_file_content(module_file, logger=LOG, translater=True)
        action_content[0] = {'action_RP': action_RP} | action_content[0] #添加相对路径信息，'|' Operator (Python 3.9+)
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
        save_file_content(module_file, module_content, logger=LOG, translater=True)
        LOG.trace(f'Add action info to the "step" section of the {module_file}')

    def __move_actionInfo_to(self, move_index: int,  to_index: int):
        """ 向 module 文件(step)中特定索引插入 action 信息"""
        moduleItem = self.topLevelItem(0)
        content = load_file_content(moduleItem.path, logger=LOG, translater=True)
        removed_action = content['step'].pop(move_index) # 根据子项索引在文件中删除对应位置上的信息
        content['step'].insert(to_index, removed_action)
        save_file_content(moduleItem.path, content, logger=LOG, translater=True)
        LOG.trace(f'Action info at "step" index {move_index} move to index {move_index} successfully at {moduleItem.path}')

    @typing.override
    def edit(self, index, trigger, event):
        """ 仅允许编辑第3列的文本 """
        if index.column() == 2:
            return super().edit(index, trigger, event)
        return False
    
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
            if draggedItem.type == 'action':
                event.accept()
    
    @typing.override
    def dragMoveEvent(self, event):
        """ 
        组件内移动事件 
        """
        item = self.itemAt(event.pos())
        if item:
            can_accept = item.acceptDrops
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
        modulePath = self.topLevelItem(0).path
        if item:
            can_accept = item.acceptDrops
            if can_accept:
                # 获取拖动源(因为有跨组件拖拽)
                source = event.source()
                grandparent = source.parent().parent() # 根据 UI 结构获取祖父级组件
                from src.views.dock import ActionDock
                if isinstance(source, QTreeWidget) and isinstance(grandparent, ActionDock): # 拖动源为关键字区域
                    # 通过当前选择的项来识别被拖动的子项
                    draggedItem = source.currentItem()
                    if draggedItem.type == 'action':
                        if item.text(0) == self.tr("测试步骤"): # 放置目标项类型一
                            newItem = ActionItem(item, data=('action', draggedItem.path, False, True), editable=True, param_editable=True) # 创建一个新的子项，放置到最后
                            self.__add_action_to_module(draggedItem.path, modulePath) # 将 action 信息写入 module
                        elif item.type == 'action': # 放置目标项类型二
                            parentItem = item.parent()
                            itemIndex = parentItem.indexOfChild(item)
                            newItem = ActionItem(parentItem, data=('action', draggedItem.path, False, True), editable=True, param_editable=True)
                            parentItem.insertChild(itemIndex + 1, newItem) # 在放置目标子项的下方插入
                            self.__add_action_to_module(draggedItem.path, modulePath, itemIndex + 1)
                        # 确认并完成当前的拖放操作
                        event.acceptProposedAction()
                elif isinstance(source, QTreeWidget) and isinstance(grandparent, EditDock): # 拖动源为编辑区域
                    # 通过当前选择的项来识别被拖动的子项
                    draggedItem = source.currentItem()
                    if draggedItem.type == 'action': # 被允许放置的类型当前只有 action
                        if item.text(0) == self.tr("测试步骤"): # 放置目标项类型一
                            draggedItemIndex = item.indexOfChild(draggedItem)
                            tempItem = item.takeChild(draggedItemIndex)
                            item.insertChild(0, tempItem) # 在第一项放置
                            tempItem.setFirstColumnSpanned(True)
                            self.__move_actionInfo_to(draggedItemIndex, 0)
                        elif item.type == 'action': # 放置目标项类型二
                            parentItem = item.parent() # 拖动项与放置目标项同级，故使用相同的父级
                            itemIndex = parentItem.indexOfChild(item)
                            draggedItemIndex = parentItem.indexOfChild(draggedItem)
                            tempItem = parentItem.takeChild(draggedItemIndex) # 拿起拖动项
                            # 计算删除拖拽项后，放置目标项的索引
                            if draggedItemIndex < itemIndex: # 拖拽项在放置目标项的上方, 放置目标项此时上移 index - 1
                                itemIndex = itemIndex - 1
                            else: # 拖拽项在放置目标项的下方，放置目标项索引不变
                                itemIndex = itemIndex
                            # 放置子项
                            if draggedItemIndex - itemIndex != 1:
                                parentItem.insertChild(itemIndex + 1, tempItem) # 在放置目标子项的下方创建同级子项
                                tempItem.setFirstColumnSpanned(True)
                                self.__move_actionInfo_to(draggedItemIndex, itemIndex + 1)
                            else: # 拖拽项在放置目标项下方，且两项相邻，则交换两项位置
                                parentItem.insertChild(itemIndex, tempItem) # 在放置目标子项的下方创建同级子项
                                tempItem.setFirstColumnSpanned(True)
                                self.__move_actionInfo_to(draggedItemIndex, itemIndex)
                        # 确认并完成当前的拖放操作
                        event.acceptProposedAction()
            else:
                # 如果组件不接受放置，拒绝放置操作
                event.ignore()
        else:
            # 如果没有拖动目标项（即拖动到了空白区域），拒绝放置操作
            event.ignore()
        self.itemChanged.connect(self.on_item_changed) # 重新开启