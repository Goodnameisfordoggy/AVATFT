'''
Author: HDJ
StartDate: please fill in
LastEditTime: 2024-08-31 00:13:19
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
import yaml
from PySide6.QtWidgets import (
    QApplication, QLabel, QMainWindow, QDockWidget, QVBoxLayout, QWidget, QLineEdit, QTreeWidget
    )
from PySide6.QtGui import QScreen
from PySide6.QtCore import Qt
from treeWidgetItem import TreeWidgetItem

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
        self.tree.setColumnCount(3) # 列数
        self.tree.setHeaderLabels(['参数描述', '参数名称', '参数值'])
        # # 拖拽功能
        # self.tree.setDragEnabled(True) # 能否拖拽
        # self.tree.setAcceptDrops(True) # 能否放置
        # self.tree.setDropIndicatorShown(True) # 是否启用放置指示器
        # self.tree.setDefaultDropAction(Qt.LinkAction)
    
    def display_action_details(self, action_path:str):
        """ 
        展示action的详细信息 
        
        action_path: 由信号携带
        """
        # 清空树控件
        self.tree.clear()
        # 读取 YAML 文件
        with open(action_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        # 创建action子项
        actionItem = TreeWidgetItem(self.tree, [config[0]['describe']]) # 配置文件(yaml)有列表结构
        actionItem.setFirstColumnSpanned(True)  # 合并三列
        try:
            parameterItemsText = [[config[0]['params_describe'][key], key, value] for key, value in config[0]['params'].items()]
        except KeyError:
            print(f'文件参数缺失：{action_path}')
            return
            
        for parameterItemText in parameterItemsText:
            parameterItem = TreeWidgetItem(actionItem, parameterItemText)

        # 展开子项
        actionItem.setExpanded(True)
        # 自动调整所有列的宽度
        self.tree.resizeColumnToContents(0)
        self.tree.resizeColumnToContents(1)
        self.tree.resizeColumnToContents(2)
    
    def display_module_details(self, module_path:str):
        print("display_module_details")
        # 清空树控件
        self.tree.clear()
        # 读取 YAML 文件
        with open(module_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
            print(config)
        # 创建action子项
        rootAction1 = TreeWidgetItem(self.tree, ['用例信息'])
        root1Child1 = TreeWidgetItem(rootAction1, ['测试用例描述', 'describe', str(config['info']['describe'])], editable=True)
        root1Child2 = TreeWidgetItem(rootAction1, ['测试用例编号', 'id', str(config['info']['id'])], editable=True)
        root1Child3 = TreeWidgetItem(rootAction1, ['测试用例标题', 'title', str(config['info']['title'])], editable=True)

        rootAction2 = TreeWidgetItem(self.tree, ['运行设置'])
        root2Child1 = TreeWidgetItem(rootAction2, [str(config['config'][0]['describe'])])
        child1Action1 = TreeWidgetItem(root2Child1, ['是否启用此配置', 'flag', str(config['config'][0]['params']['flag'])], editable=True)
        child1Action2 = TreeWidgetItem(root2Child1, ['用例跳过原因', 'reason', str(config['config'][0]['params']['reason'])], editable=True)
        root2Child2 = TreeWidgetItem(rootAction2, [str(config['config'][1]['describe'])])
        child2Action1 = TreeWidgetItem(root2Child2, ['是否启用此配置', 'flag', str(config['config'][1]['params']['flag'])], editable=True)
        child2Action2 = TreeWidgetItem(root2Child2, ['用例标签名称', 'markname', str(config['config'][1]['params']['markname'])], editable=True)
        root2Child3 = TreeWidgetItem(rootAction2, [str(config['config'][2]['describe'])])
        child3Action1 = TreeWidgetItem(root2Child3, ['是否启用此配置', 'flag', str(config['config'][2]['params']['flag'])], editable=True)
        child3Action2 = TreeWidgetItem(root2Child3, ['前后置函数名称', 'fixtures', str(config['config'][2]['params']['fixtures'])], editable=True)
        root2Child4 = TreeWidgetItem(rootAction2, [str(config['config'][3]['describe'])])
        child4Action1 = TreeWidgetItem(root2Child4, ['是否启用此配置', 'flag', str(config['config'][3]['params']['flag'])], editable=True)
        child4Action2 = TreeWidgetItem(root2Child4, ['数据驱动文件名称', 'filename', str(config['config'][3]['params']['filename'])], editable=True)
        child4Action3 = TreeWidgetItem(root2Child4, ['数据驱动文件Sheet', 'sheetname', str(config['config'][3]['params']['sheetname'])], editable=True)
        
        rootAction3 = TreeWidgetItem(self.tree, ['测试步骤'], (None,None,True,True))


class TreeWidget(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.setDragEnabled(True) # 能否拖拽
        self.setAcceptDrops(True) # 能否放置
        self.setDropIndicatorShown(True) # 是否启用放置指示器
        self.setDefaultDropAction(Qt.CopyAction) # 放置操作 (MoveAction, CopyAction, LinkAction: 创建一个链接或引用)
        
    def edit(self, index, trigger, event):
        # 仅允许编辑第3列的文本
        if index.column() == 2:
            return super().edit(index, trigger, event)
        return False
    
    def dragEnterEvent(self, event):
        """ 接受拖拽操作事件 """
        item = self.itemAt(event.pos())
        if item:
            can_accept = item.data(2, Qt.UserRole)
            if can_accept:
                event.acceptProposedAction()
            else:
                event.ignore()
        else:
            event.ignore()
        # event.accept()

    # def dragMoveEvent(self, event):
    #     """ 组件内移动事件"""
    #     item = self.itemAt(event.pos())
    #     if item:
    #         can_accept = item.data(2, Qt.UserRole)
    #         if can_accept:
    #             event.acceptProposedAction()
    #         else:
    #             event.ignore()
    #     else:
    #         event.ignore()

    def dropEvent(self, event):
        """ 放置事件 """
        target_item = self.itemAt(event.pos())
        dragged_item = self.currentItem()
        
        if target_item:
            can_accept = target_item.data(3, Qt.UserRole)
            if can_accept:
                event.acceptProposedAction()
                parent_item = target_item.parent()

                # 如果目标项没有父项，则插入到根项中
                if parent_item is None:
                    index = self.indexOfTopLevelItem(target_item) + 1
                    self.takeTopLevelItem(self.indexOfTopLevelItem(dragged_item))
                    self.insertTopLevelItem(index, dragged_item)
                else:
                    index = parent_item.indexOfChild(target_item) + 1
                    self.takeTopLevelItem(self.indexOfTopLevelItem(dragged_item))
                    parent_item.insertChild(index, dragged_item)
            else:
                event.ignore()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication([])
    window = EditDock()
    window.show()
    app.exec()